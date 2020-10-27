import time
from typing import Optional, Callable, List, Awaitable

from pydantic import Field

import config
from pycurd.const import QUERY_OP_COMPARE
from pycurd.crud.base_crud import PermInfo
from pycurd.crud.query_result_row import QueryResultRow
from pycurd.query import QueryInfo, ConditionExpr
from pycurd.types import RecordMapping, IDList
from pycurd.values import ValuesToWrite

from model._post import POST_STATE, POST_VISIBLE


def get_time():
    return int(time.time())


class Post(RecordMapping):
    id: bytes
    state: int
    visible: int
    time: int = Field(default_factory=get_time)
    user_id: Optional[bytes]

    @classmethod
    async def on_insert(
            cls,
            values_lst: List['ValuesToWrite'],
            when_complete: List[Callable[[IDList], Awaitable]],
            perm: 'PermInfo' = None
    ):
        if perm and perm.user:
            for values in values_lst:
                values['user_id'] = perm.user.id

                if not config.POST_ID_GENERATOR == config.SQLSerialGenerator:
                    values['id'] = config.POST_ID_GENERATOR().digest()

    @classmethod
    async def on_query(cls, info: 'QueryInfo', perm: 'PermInfo' = None):
        from crud.roles import ordinary_roles

        if perm and perm.role in ordinary_roles:
            # state 约束
            info.conditions.items.append(
                ConditionExpr(cls.state, QUERY_OP_COMPARE.GT, POST_STATE.APPLY)
            )

            # visible 约束（动态）
            roles = {perm.role} if not perm.user else set(perm.user.roles)
            if roles & {'superuser', 'admin'}:
                return

            if roles & {'inactive_user', 'user', 'wiki_editor'}:
                visible_limit = POST_VISIBLE.ADMIN_ONLY
            else:
                visible_limit = POST_VISIBLE.USER_ONLY

            info.conditions.items.extend([
                ConditionExpr(cls.visible, QUERY_OP_COMPARE.GT, POST_VISIBLE.HIDE),
                ConditionExpr(cls.visible, QUERY_OP_COMPARE.LT, visible_limit),
            ])

    @classmethod
    async def on_read(
            cls,
            info: 'QueryInfo',
            when_complete: List[Callable[[List[QueryResultRow]], Awaitable]],
            perm: 'PermInfo' = None
    ):
        # TODO: 未登录不能查看约束
        # if record.get('visible') == POST_VISIBLE.CONTENT_IF_LOGIN:
        #     available_columns.remove('content')

        # TODO: 如果查询的是自己，附带部分信息
        # from slim.utils import get_bytes_from_blob
        #
        # def func(ability: Ability, user, query: 'SQLQueryInfo'):
        #     for i in query.conditions.find('id'):
        #         if i[1] == SQL_OP.EQ and i[2] == user.id.hex():
        #             query.select.add('email')
        #             query.select.add('phone')
        #             query.select.add('access_time')
        #             query.select.add('is_new_user')
        #             query.select.add('phone_verified')
        #             query.select.add('change_nickname_chance')
        pass

    @classmethod
    async def on_update(
            cls,
            info: 'QueryInfo',
            values: 'ValuesToWrite',
            when_before_update: List[Callable[[IDList], Awaitable]],
            when_complete: List[Callable[[], Awaitable]],
            perm: 'PermInfo' = None
    ):
        from crud.roles import ordinary_roles

        if perm and perm.role in ordinary_roles:
            # 不准写入其他用户发布的内容
            info.conditions.items.append(
                ConditionExpr(cls.user_id, QUERY_OP_COMPARE.EQ, perm.user.id)
            )

            # 如果当前post是用户，只能写自己
            from crud.schemas.user import User
            if cls == User:
                info.conditions.items.append(
                    ConditionExpr(cls.id, QUERY_OP_COMPARE.EQ, perm.user.id)
                )

            # # 阻止superuser写入superuser或更高权限用户组
            # if user:
            #     if record.get('group') in (USER_GROUP.SUPERUSER, USER_GROUP.ADMIN):
            #         # 只允许写这两列
            #         available_columns.clear()
            #         available_columns.update(filter(lambda x: x in {'credit', 'repute'}, available_columns))
            # return True
