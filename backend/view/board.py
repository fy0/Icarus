import time
from typing import Mapping, Dict, List
import config
from model._post import POST_TYPES
from model.statistic import statistic_new
from slim.base.permission import Permissions, DataRecord
from slim.base.sqlquery import SQLValuesToWrite
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.board import Board
from view import route, ValidateForm
from wtforms import StringField, validators as va

from view.permissions import visitor, normal_user, super_user, admin
from view.user import UserMixin


class BoardForm(ValidateForm):
    name = StringField('板块名', validators=[va.required(), va.Length(1, 30)])

    brief = StringField('简介', validators=[
        # va.required(),  # 注：必填和下面的0冲突，长度为零会视为空
        va.Length(0, 256)
    ])

    desc = StringField('详细说明', validators=[va.Length(0, 1024)])


@route('board')
class BoardView(PeeweeView, UserMixin):
    model = Board
    LIST_PAGE_SIZE = -1

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'statistic', 's')
        cls.add_soft_foreign_key('id', 'statistic24h', 's24')
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('parent_id', 'board')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permission.add(visitor)
        permission.add(normal_user)
        permission.add(super_user)
        permission.add(admin)

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        for values in values_lst:
            form = BoardForm(**values)
            if not form.validate():
                return RETCODE.FAILED, form.errors

            if not config.POST_ID_GENERATOR == config.AutoGenerator:
                values['id'] = config.POST_ID_GENERATOR().digest()
            values['time'] = int(time.time())
            values['user_id'] = self.current_user.id

    async def after_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite], records: List[DataRecord]):
        for record in records:
            # 添加统计记录
            statistic_new(POST_TYPES.BOARD, record['id'])
