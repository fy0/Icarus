from typing import Dict, List
import time
import config
from model.post import POST_TYPES
from model.statistic import statistic_new, statistic_add_topic, statistic_add_topic_click, statistic_move_topic
from model.topic import Topic
from slim.base.permission import Permissions, DataRecord
from slim.base.sqlquery import SQLValuesToWrite
from slim.base.view import SQLQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin, dict_filter_inplace
from view import route, ValidateForm
from wtforms import validators as va, StringField, IntegerField

from view.permissions import visitor, normal_user, super_user, admin
from view.user import UserMixin


class TopicNewForm(ValidateForm):
    title = StringField('标题', validators=[va.required(), va.Length(1, config.TOPIC_TITLE_LENGTH_MAX)])

    content = StringField('正文', validators=[
        va.required(),
        va.Length(1, config.TOPIC_CONTENT_LENGTH_MAX)
    ])

    sticky_weight = IntegerField('置顶权重', validators=[])
    weight = IntegerField('排序权重', validators=[])


class TopicEditForm(ValidateForm):
    title = StringField('标题', validators=[va.optional(), va.Length(1, config.TOPIC_TITLE_LENGTH_MAX)])

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
        permission.add(visitor)
        permission.add(normal_user)
        permission.add(super_user)
        permission.add(admin)

    async def get(self):
        await super().get()
        if self.ret_val['code'] == RETCODE.SUCCESS:
            vals = getattr(self, '_val_bak', None)
            if vals: statistic_add_topic_click(*vals)

    def after_read(self, records: List[DataRecord]):
        for i in records:
            # TODO: FIX
            self._val_bak = [i['id'], i['board_id']]

    def after_update(self, raw_post: Dict, values: SQLValuesToWrite, old_records: List[DataRecord], records: List[DataRecord]):
        for old_record, record in zip(old_records, records):
            if old_record['board_id'] != record['board_id']:
                statistic_move_topic(old_record['board_id'], record['board_id'], record['id'])

            Topic.update(edit_count=Topic.edit_count + 1).where(Topic.id == record['id']).execute()

    def before_update(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        form = TopicEditForm(**raw_post)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        # 防止置空提交，因为这里这两项的校验是 optional
        if 'title' in values and not values['title']:
            del values['title']
        if 'content' in values and not values['content']:
            del values['content']

        if 'topic' in values or 'content' in values:
            values['edit_time'] = int(time.time())
            values['last_edit_user_id'] = self.current_user.id

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
        form = TopicNewForm(**raw_post)
        if not form.validate():
            return RETCODE.FAILED, form.errors
        values['user_id'] = self.current_user.id

        # 以下通用
        if not config.POST_ID_GENERATOR == config.AutoGenerator:
            values['id'] = config.POST_ID_GENERATOR().digest()
        values['time'] = int(time.time())
        values['weight'] = Topic.weight_gen()

    def after_insert(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]
        statistic_add_topic(record['board_id'], record['id'])

        # 添加统计记录
        statistic_new(POST_TYPES.TOPIC, record['id'])


'''
from slim.utils.debug import Debug 

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''
