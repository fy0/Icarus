from typing import Dict
import time
import config
from model.post import POST_TYPES
from model.statistic import statistic_new, statistic_add_topic, statistic_add_topic_click
from model.topic import Topic
from slim.base.permission import Permissions, Ability, AbilityRecord, AbilityColumn, A
from slim.base.view import ParamsQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin, dict_filter_inplace
from view import route, ValidateForm
from wtforms import validators as va, StringField, IntegerField
from view.user import UserMixin


class TopicForm(ValidateForm):
    title = StringField('标题', validators=[va.required(), va.Length(1, config.TOPIC_TITLE_LENGTH_MAX)])

    content = StringField('正文', validators=[
        va.required(),
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
        visitor = Ability(None, {
            'topic': {
                'id': ['query', 'read'],
                'title': ['read'],
                'user_id': ['query', 'read'],
                'board_id': ['query', 'read'],
                'time': ['read'],
                'state': ['read'],

                'edit_time': ['read'],
                'last_edit_user_id': ['read'],
                'content': ['read'],

                'sticky_weight': ['read'],
                'weight': ['read'],
            }
        })

        normal_user = Ability('user', {
            'topic': {
                'id': [A.QUERY, A.READ, A.CREATE],
                'title': [A.READ, A.CREATE, A.WRITE],
                'user_id': [A.QUERY, A.READ, A.CREATE],
                'board_id': [A.QUERY, A.READ, A.CREATE, A.WRITE],
                'time': [A.READ, A.CREATE],
                'content': [A.READ, A.CREATE, A.WRITE],
            }
        }, based_on=visitor)

        def is_users_post(ability, user, cur_action, record: AbilityRecord) -> bool:
            if user:
                return record.get('id') == user.id

        normal_user.add_record_rule(
            ['read', 'write', A.CREATE],
            AbilityColumn('topic', 'title'),
            func=is_users_post
        )

        normal_user.add_record_rule(
            ['read', 'write', A.CREATE],
            AbilityColumn('topic', 'content'),
            func=is_users_post
        )

        normal_user.add_record_rule(
            ['query', 'read', 'write'],
            AbilityColumn('topic', 'state'),
            func=is_users_post
        )

        admin = Ability('admin', {
            'topic': '*'
        })

        permission.add(visitor)
        permission.add(normal_user)
        permission.add(admin)

    async def get(self):
        await super().get()
        if self.ret_val['code'] == RETCODE.SUCCESS:
            vals = getattr(self, '_val_bak', None)
            if vals: statistic_add_topic_click(*vals)

    def handle_read(self, values: Dict):
        self._val_bak = [values['id'], values['board_id']]

    def handle_query(self, info: ParamsQueryInfo):
        pass

    def handle_update(self, values: Dict):
        form = TopicForm(**values)
        if not form.validate():
            return RETCODE.FAILED, form.errors
        dict_filter_inplace(values, ('title', 'board_id', 'content'))

        values['board_id'] = to_bin(values['board_id'])
        #values['user_id'] = self.current_user.id

    def handle_insert(self, values: Dict):
        form = TopicForm(**values)
        if not form.validate():
            return RETCODE.FAILED, form.errors
        dict_filter_inplace(values, ('title', 'board_id', 'content'))

        values['board_id'] = to_bin(values['board_id'])
        values['user_id'] = self.current_user.id

        # 以下通用
        values['id'] = config.ID_GENERATOR().digest()
        values['time'] = int(time.time())

        # 添加统计记录
        statistic_new(POST_TYPES.TOPIC, values['id'])

    def after_insert(self, values: Dict):
        statistic_add_topic(values['board_id'], values['id'])


'''
from slim.utils.debug import Debug 

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''
