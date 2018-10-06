from permissions.roles import *
from model._post import POST_STATE, POST_VISIBLE
from permissions.tables._vars import post_visible_work
from slim.base.permission import Ability, A, DataRecord
from slim.base.sqlquery import SQLQueryInfo, SQL_OP

post_visible_work('comment')
