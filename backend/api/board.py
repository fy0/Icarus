import time
import config
from typing import Mapping, Dict, List

from app import app
from model._post import POST_TYPES
from model.post_stats import post_stats_new
from slim.base.permission import Permissions, DataRecord
from slim.base.sqlquery import SQLValuesToWrite
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from model.board import Board
from api import ValidateForm
from wtforms import StringField, validators as va
from model.manage_log import ManageLog, MANAGE_OPERATION as MOP
from api.user import UserViewMixin


class BoardForm(ValidateForm):
    name = StringField('板块名', validators=[va.required(), va.Length(1, 30)])

    brief = StringField('简介', validators=[
        # va.required(),  # 注：必填和下面的0冲突，长度为零会视为空
        va.Length(0, 256)
    ])

    desc = StringField('详细说明', validators=[va.Length(0, 1024)])


@app.route.view('board')
class BoardView(PeeweeView, UserViewMixin):
    model = Board
    LIST_PAGE_SIZE = -1

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'post_stats', 's')
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('parent_id', 'board')

    async def before_insert(self, values_lst: List[SQLValuesToWrite]):
        for values in values_lst:
            form = BoardForm(**values)
            if not form.validate():
                return self.finish(RETCODE.FAILED, form.errors)

            if not config.POST_ID_GENERATOR == config.SQLSerialGenerator:
                values['id'] = config.POST_ID_GENERATOR().digest()
            values['time'] = int(time.time())
            values['user_id'] = self.current_user.id

    async def after_update(self, values: SQLValuesToWrite, old_records: List[DataRecord],
                           new_records: List[DataRecord]):
        for old_record, record in zip(old_records, new_records):
            # 注：此处记录不考虑可写不可读的情况。代码比较丑陋，后面改吧
            o = old_record.to_dict()
            n = record.to_dict()
            to_remove = set()
            for k, v in n.items():
                if k in o and o[k] == v:
                    to_remove.add(k)
            for k, v in o.items():
                if k in n and n[k] == v:
                    to_remove.add(k)
            for k in to_remove:
                del o[k]
                del n[k]

            # 管理日志
            ManageLog.new(self.current_user, self.current_request_role, POST_TYPES.BOARD, record['id'],
                          record['user_id'], MOP.BOARD_INFO_CHANGE, [o, n])

    async def after_insert(self, values_lst: List[SQLValuesToWrite], records: List[DataRecord]):
        for record in records:
            # 添加统计记录
            post_stats_new(POST_TYPES.BOARD, record['id'])

            # 管理日志：新建板块
            ManageLog.post_new(self, POST_TYPES.BOARD, record)
