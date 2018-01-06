import time
from typing import Mapping, Dict
import config
from model.statistic import statistic_new
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.board import Board
from view import route, ValidateForm
from wtforms import StringField, validators as va


class BoardForm(ValidateForm):
    name = StringField('板块名', validators=[va.required(), va.Length(1, 30)])

    brief = StringField('简介', validators=[
        # va.required(),  # 注：必填和下面的0冲突，长度为零会视为空
        va.Length(0, 256)
    ])

    desc = StringField('详细说明', validators=[va.Length(0, 1024)])


@route('board')
class UserView(PeeweeView):
    options = PeeweeView.options_cls(model=Board, list_page_size=-1)

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'statistic')

    @classmethod
    def handle_read(self, values: Dict):
        pass

    @classmethod
    def handle_insert(cls, values: Dict):
        form = BoardForm(**values)
        if not form.validate():
            return RETCODE.FAILED, form.errors

        values['id'] = config.ID_GENERATOR().digest()
        values['time'] = int(time.time())

        # 添加统计记录
        statistic_new(values['id'])
