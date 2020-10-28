import time
import config
from typing import Mapping, Dict, List

from api.view.curd import BaseCrudUserView
from app import app
from crud.schemas.board import Board
from model._post import POST_TYPES
from model.post_stats import post_stats_new
from slim.retcode import RETCODE
from model.board_model import BoardModel
from model.manage_log import ManageLogModel, MANAGE_OPERATION as MOP


# class BoardForm(ValidateForm):
#     name = StringField('板块名', validators=[va.required(), va.Length(1, 30)])
#
#     brief = StringField('简介', validators=[
#         # va.required(),  # 注：必填和下面的0冲突，长度为零会视为空
#         va.Length(0, 256)
#     ])
#
#     desc = StringField('详细说明', validators=[va.Length(0, 1024)])


@app.route.view('board')
class BoardView(BaseCrudUserView):
    model = Board
    LIST_PAGE_SIZE = -1

    # @classmethod
    # def ready(cls):
    #     cls.add_soft_foreign_key('id', 'post_stats', 's')
    #     cls.add_soft_foreign_key('user_id', 'user')
    #     cls.add_soft_foreign_key('parent_id', 'board')
