from typing import Dict
import time
import config
from model.board import Board
from model.topic import Topic
from slim.base.view import ParamsQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin
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
    def cls_init(cls, check_options=True):
        super().cls_init(check_options)
        cls.add_soft_foreign_key('user_id', 'user')

    def handle_read(self, values: Dict):
        pass

    def handle_query(self, info: ParamsQueryInfo):
        pass

    def handle_insert(self, values: Dict):
        form = TopicForm(**values)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        values['board_id'] = to_bin(values['board_id'])
        values['user_id'] = self.current_user.id

        # 以下通用
        values['id'] = config.ID_GENERATOR().digest()
        values['time'] = int(time.time())


'''
from slim.utils.debug import Debug

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''

TopicView.add_soft_foreign_key('user_id', 'user')
TopicView.add_soft_foreign_key('board_id', 'board')
TopicView.add_soft_foreign_key('last_edit_user_id', 'user')
