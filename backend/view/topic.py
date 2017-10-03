from typing import Dict
import time
import config
from model.topic import Topic
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from view import route, ValidateForm
from wtforms import StringField, validators as va, IntegerField


class TopicForm(ValidateForm):
    title = StringField('标题', validators=[va.required(), va.Length(1, config.TOPIC_TITLE_LENGTH_MAX)])

    content = StringField('正文', validators=[
        va.required(),
        va.Length(1, config.TOPIC_CONTENT_LENGTH_MAX)
    ])

    sticky_weight = IntegerField('置顶权重', validators=[])
    weight = IntegerField('排序权重', validators=[])


@route('topic')
class UserView(PeeweeView):
    model = Topic

    @classmethod
    def handle_read(cls, values: Dict):
        pass

    @classmethod
    def handle_insert(cls, values: Dict):
        form = TopicForm(**values)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        values['id'] = config.ID_GENERATOR().digest()
        values['time'] = int(time.time())
