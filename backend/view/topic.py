from typing import Dict, List
import time
import config
from lib.textdiff import diff
from model._post import POST_TYPES
from model.manage_log import ManageLog, MANAGE_OPERATION as MOP
from model.post_stats import post_stats_add_topic_click, post_stats_topic_move, post_stats_topic_new, post_stats_do_edit
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
        va.optional(),
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
        cls.add_soft_foreign_key('id', 'post_stats')
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
            if vals: post_stats_add_topic_click(*vals)

    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_IP, b'ic_cd_topic_new_%b', cd_if_unsuccessed=10)
    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_ACCOUNT, b'ic_cd_topic_new_account_%b', unique_id_func=same_user, cd_if_unsuccessed=10)
    async def new(self):
        return await super().new()

    def after_read(self, records: List[DataRecord]):
        for i in records:
            self._val_bak = [i['id'], i['board_id']]

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

    def after_update(self, raw_post: Dict, values: SQLValuesToWrite, old_records: List[DataRecord], records: List[DataRecord]):
        for old_record, record in zip(old_records, records):
            manage_try_add = lambda column, op: ManageLog.add_by_post_changed(
                self, column, op, POST_TYPES.TOPIC, values, old_record, record
            )
            manage_try_add_with_diff = lambda column, op: ManageLog.add_by_post_changed(
                self, column, op, POST_TYPES.TOPIC, values, old_record, record, diff_func=diff
            )

            title_changed = manage_try_add('title', MOP.POST_TITLE_CHANGE)  # 管理日志：标题编辑
            content_changed = manage_try_add_with_diff('content', MOP.POST_CONTENT_CHANGE)  # 管理日志：正文编辑

            if title_changed or content_changed:
                post_stats_do_edit(record['id'], record['user_id'])
                Topic.update(edit_count=Topic.edit_count + 1).where(Topic.id == record['id']).execute()

            manage_try_add('state', MOP.POST_STATE_CHANGE)  # 管理日志：状态修改
            manage_try_add('visible', MOP.POST_VISIBLE_CHANGE)  # 管理日志：改变可见度
            manage_try_add('awesome', MOP.TOPIC_AWESOME_CHANGE)  # 管理日志：设置精华
            manage_try_add('sticky_weight', MOP.TOPIC_STICKY_WEIGHT_CHANGE)  # 管理日志：置顶权重
            manage_try_add('weight', MOP.TOPIC_WEIGHT_CHANGE)  # 管理日志：修改权重

            # 管理日志：移动板块
            if manage_try_add('board_id', MOP.TOPIC_BOARD_MOVE):
                post_stats_topic_move(old_record['board_id'], record['board_id'], record['id'])

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

        # if self.do_mentions:
        #     self.do_mentions(record['user_id'], POST_TYPES.TOPIC, record['id'], {
        #         'title': record['title'],
        #     })

        # 添加统计记录
        post_stats_topic_new(record['board_id'], record['id'])


'''
from slim.utils.debug import Debug 

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''
