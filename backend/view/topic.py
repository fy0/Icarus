from typing import Dict
import time
import config
from model.post import POST_TYPES
from model.statistic import statistic_new, statistic_add_topic, statistic_add_topic_click
from model.topic import Topic
from slim.base.permission import Permissions, DataRecord
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

    def after_read(self, dbdata: Dict, values: Dict):
        self._val_bak = [values['id'], values['board_id']]

    def after_update(self, values: Dict):
        # Topic.update(edit_count = Topic.edit_count + 1).execute()
        pass

    def before_update(self, raw_post: Dict, values: Dict):
        form = TopicEditForm(**raw_post)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        # 防止置空提交，因为这里这两项的校验是 optional
        if 'title' in values and not values['title']:
            del values['title']
        if 'content' in values and not values['content']:
            del values['content']

        if 'board_id' in values:
            values['board_id'] = to_bin(values['board_id'])

        if 'topic' in values or 'content' in values:
            values['edit_time'] = int(time.time())
            values['last_edit_user_id'] = self.current_user.id
            # TODO: edit_count

    def before_insert(self, raw_post: Dict, values: Dict):
        form = TopicNewForm(**raw_post)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        values['board_id'] = to_bin(values['board_id'])
        values['user_id'] = self.current_user.id

        # 以下通用
        if not config.POST_ID_GENERATOR == config.AutoGenerator:
            values['id'] = config.POST_ID_GENERATOR().digest()
        values['time'] = int(time.time())
        values['weight'] = Topic.weight_gen()

    def after_insert(self, raw_post: Dict, dbdata: DataRecord, values: Dict):
        statistic_add_topic(values['board_id'], values['id'])

        # 添加统计记录
        statistic_new(POST_TYPES.TOPIC, values['id'])


'''
from slim.utils.debug import Debug 

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''
