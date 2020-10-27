from typing import Optional, List, Callable, Awaitable

import config
from api import run_in_thread
from crud.schemas._post import Post
from model import esdb
from model._post import POST_TYPES
from model.manage_log import ManageLogModel
from model.post_stats import post_stats_new
from pycurd.crud.base_crud import PermInfo
from pycurd.query import QueryInfo
from pycurd.types import IDList
from pycurd.values import ValuesToWrite


class Board(Post):
    name: str = None
    parent_id: Optional[bytes]
    brief: Optional[str]
    desc: Optional[str]
    weight: int = 0
    color: Optional[bytes]
    category: Optional[str]
    can_post_rank: int = 0

    @classmethod
    async def on_insert(
            cls,
            values_lst: List['ValuesToWrite'],
            when_complete: List[Callable[[IDList], Awaitable]],
            perm: 'PermInfo' = None
    ):
        await super().on_insert(values_lst, when_complete, perm)

        async def on_complete(id_lst: IDList):
            # 创建完成后添加入日志
            for id_ in id_lst:
                post_stats_new(POST_TYPES.BOARD, id_)

                # TODO: 管理日志：新建板块
                # ManageLogModel.post_new(self, POST_TYPES.BOARD, record)

        when_complete.append(on_complete)

    @classmethod
    async def on_update(
            cls,
            info: 'QueryInfo',
            values: 'ValuesToWrite',
            when_before_update: List[Callable[[IDList], Awaitable]],
            when_complete: List[Callable[[], Awaitable]],
            perm: 'PermInfo' = None
    ):
        pass

        '''
        async def after_update(self, values: 'SQLValuesToWrite', old_records: List['DataRecord'],
                               new_records: List['DataRecord']):
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
                ManageLogModel.new(self.current_user, self.current_request_role, POST_TYPES.BOARD, record['id'],
                                   record['user_id'], MOP.BOARD_INFO_CHANGE, [o, n])
        '''
