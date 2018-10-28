from typing import Dict, List
import time
import config
from model._post import POST_TYPES
from model.log_manage import ManageLog, MANAGE_OPERATION as MOP
from model.statistic import statistic_new, statistic_add_topic, statistic_add_topic_click, statistic_move_topic
from model.topic import Topic
from slim.base.permission import Permissions, DataRecord
from slim.base.sqlquery import SQLValuesToWrite
from slim.base.view import SQLQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin, dict_filter_inplace
from view import route, ValidateForm, cooldown, same_user
from wtforms import validators as va, StringField, IntegerField

from view.mention import check_content_mention
from permissions import permissions_add_all
from view.user import UserMixin


class TopicNewForm(ValidateForm):
    title = StringField('标题', validators=[
        va.required(),
        va.Length(config.TOPIC_TITLE_LENGTH_MIN, config.TOPIC_TITLE_LENGTH_MAX)
    ])

    content = StringField('正文', validators=[
        va.required(),
        va.Length(1, config.TOPIC_CONTENT_LENGTH_MAX)
    ])

    sticky_weight = IntegerField('置顶权重', validators=[])
    weight = IntegerField('排序权重', validators=[])


class TopicEditForm(ValidateForm):
    title = StringField('标题', validators=[
        va.required(),
        va.Length(config.TOPIC_TITLE_LENGTH_MIN, config.TOPIC_TITLE_LENGTH_MAX)
    ])

    content = StringField('正文', validators=[
        va.optional(),
        va.Length(1, config.TOPIC_CONTENT_LENGTH_MAX)
    ])

    sticky_weight = IntegerField('置顶权重', validators=[])
    weight = IntegerField('排序权重', validators=[])


@route('topic')
class TopicView(UserMixin, PeeweeView):
    model = Topic

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'statistic')
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('board_id', 'board')
        cls.add_soft_foreign_key('last_edit_user_id', 'user')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)

    async def prepare(self):
        self.do_mentions = None

    async def get(self):
        await super().get()
        if self.ret_val['code'] == RETCODE.SUCCESS:
            vals = getattr(self, '_val_bak', None)
            if vals: statistic_add_topic_click(*vals)

    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_IP, b'ic_cd_topic_new_%b', cd_if_unsuccessed=10)
    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_ACCOUNT, b'ic_cd_topic_new_account_%b', unique_id_func=same_user, cd_if_unsuccessed=10)
    async def new(self):
        return await super().new()

    def after_read(self, records: List[DataRecord]):
        for i in records:
            # TODO: FIX
            self._val_bak = [i['id'], i['board_id']]

    def after_update(self, raw_post: Dict, values: SQLValuesToWrite, old_records: List[DataRecord], records: List[DataRecord]):
        for old_record, record in zip(old_records, records):
            if 'content' in values:
                # 管理日志：正文编辑
                ManageLog.new(self.current_user, self.current_role, POST_TYPES.TOPIC, record['id'], record['user_id'],
                              MOP.TOPIC_CONTENT_CHANGE, None)
                Topic.update(edit_count=Topic.edit_count + 1).where(Topic.id == record['id']).execute()

            if 'title' in values:
                # 管理日志：标题编辑
                ManageLog.new(self.current_user, self.current_role, POST_TYPES.TOPIC, record['id'], record['user_id'],
                              MOP.TOPIC_TITLE_CHANGE, None)

            # 管理日志：改变状态
            ManageLog.add_by_post_changed(self, 'state', MOP.POST_STATE_CHANGE, POST_TYPES.TOPIC,
                                          values, old_record, record)

            # 管理日志：改变可见度
            ManageLog.add_by_post_changed(self, 'visible', MOP.POST_VISIBLE_CHANGE, POST_TYPES.TOPIC,
                                          values, old_record, record)

            # 管理日志：移动板块
            if ManageLog.add_by_post_changed(self, 'board_id', MOP.TOPIC_BOARD_MOVE, POST_TYPES.TOPIC,
                                             values, old_record, record):
                statistic_move_topic(old_record['board_id'], record['board_id'], record['id'])

            # 管理日志：设置精华
            ManageLog.add_by_post_changed(self, 'awesome', MOP.TOPIC_AWESOME_CHANGE, POST_TYPES.TOPIC,
                                          values, old_record, record)

            # 管理日志：置顶权重
            ManageLog.add_by_post_changed(self, 'sticky_weight', MOP.TOPIC_STICKY_WEIGHT_CHANGE, POST_TYPES.TOPIC,
                                          values, old_record, record)

            # 管理日志：修改权重
            ManageLog.add_by_post_changed(self, 'weight', MOP.TOPIC_WEIGHT_CHANGE, POST_TYPES.TOPIC,
                                          values, old_record, record)

    def before_update(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]
        form = TopicEditForm(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        # 防止置空提交，因为这里这两项的校验是 optional
        if 'title' in values:
            if not values['title']:
                del values['title']
            elif values['title'] == record['title']:
                del values['title']
        if 'content' in values:
            if not values['content']:
                del values['content']
            elif values['content'] == record['content']:
                del values['content']

        if 'topic' in values or 'content' in values:
            values['edit_time'] = int(time.time())
            values['last_edit_user_id'] = self.current_user.id

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
        form = TopicNewForm(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)
        values['user_id'] = self.current_user.id

        # 以下通用
        if not config.POST_ID_GENERATOR == config.AutoGenerator:
            values['id'] = config.POST_ID_GENERATOR().digest()
        values['time'] = int(time.time())
        values['weight'] = await Topic.weight_gen()
        values['update_time'] = int(time.time())

        # 主题不再支持 @
        # values['content'], self.do_mentions = check_content_mention(values['content'])

    def after_insert(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]

        if self.do_mentions:
            self.do_mentions(record['user_id'], POST_TYPES.TOPIC, record['id'], {
                'title': record['title'],
            })

        statistic_add_topic(record['board_id'], record['id'])

        # 添加统计记录
        statistic_new(POST_TYPES.TOPIC, record['id'])


'''
from slim.utils.debug import Debug 

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''
