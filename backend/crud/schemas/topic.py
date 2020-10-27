import time
from typing import Optional, List, Callable, Awaitable

import config
from api import run_in_thread
from crud.schemas._post import Post
from model import esdb
from model.post_stats import post_stats_add_topic_click, post_stats_topic_new
from model.topic_model import TopicModel
from pycurd.crud.base_crud import PermInfo
from pycurd.crud.query_result_row import QueryResultRow
from pycurd.query import QueryInfo
from pycurd.types import IDList
from pycurd.values import ValuesToWrite


class Topic(Post):
    title: str
    board_id: bytes

    edit_count: int
    edit_time: Optional[int]
    last_edit_user_id: Optional[bytes]
    content: str

    awesome: int = 0
    sticky_weight: int = 0
    weight: int = 0
    update_time: Optional[int]

    @classmethod
    async def on_update(
            cls,
            info: 'QueryInfo',
            values: 'ValuesToWrite',
            when_before_update: List[Callable[[IDList], Awaitable]],
            when_complete: List[Callable[[], Awaitable]],
            perm: 'PermInfo' = None
    ):
        # 写入最后编辑者和编辑时间
        if 'topic' in values or 'content' in values:
            values['edit_time'] = int(time.time())
            if perm and perm.user:
                values['last_edit_user_id'] = perm.user.id

        '''
        async def after_update(self, values: SQLValuesToWrite, old_records: List['DataRecord'],
                               new_records: List['DataRecord']):
            for old_record, record in zip(old_records, new_records):
                manage_try_add = lambda column, op: ManageLogModel.add_by_post_changed(
                    self, column, op, POST_TYPES.TOPIC, values, old_record, record
                )
                manage_try_add_with_diff = lambda column, op: ManageLogModel.add_by_post_changed(
                    self, column, op, POST_TYPES.TOPIC, values, old_record, record, diff_func=diff
                )

                title_changed = manage_try_add('title', MOP.POST_TITLE_CHANGE)  # 管理日志：标题编辑
                content_changed = manage_try_add_with_diff('content', MOP.POST_CONTENT_CHANGE)  # 管理日志：正文编辑

                if title_changed or content_changed:
                    post_stats_do_edit(record['id'], record['user_id'])
                    TopicModel.update(edit_count=TopicModel.edit_count + 1).where(TopicModel.id == record['id']).execute()

                manage_try_add('state', MOP.POST_STATE_CHANGE)  # 管理日志：状态修改
                manage_try_add('visible', MOP.POST_VISIBLE_CHANGE)  # 管理日志：改变可见度
                manage_try_add('awesome', MOP.TOPIC_AWESOME_CHANGE)  # 管理日志：设置精华
                manage_try_add('sticky_weight', MOP.TOPIC_STICKY_WEIGHT_CHANGE)  # 管理日志：置顶权重
                manage_try_add('weight', MOP.TOPIC_WEIGHT_CHANGE)  # 管理日志：修改权重

                # 管理日志：移动板块
                if manage_try_add('board_id', MOP.TOPIC_BOARD_MOVE):
                    post_stats_topic_move(old_record['board_id'], record['board_id'], record['id'])

                if config.SEARCH_ENABLE:
                    run_in_thread(esdb.es_update_topic, record['id'])
        '''

    @classmethod
    async def on_insert(
            cls,
            values_lst: List['ValuesToWrite'],
            when_complete: List[Callable[[IDList], Awaitable]],
            perm: 'PermInfo' = None
    ):
        await super().on_insert(values_lst, when_complete, perm)
        # 提升权重上限，刷新编辑时间
        for values in values_lst:
            values['weight'] = await TopicModel.weight_gen()
            values['update_time'] = int(time.time())

            # 主题不再支持 @
            # values['content'], self.do_mentions = check_content_mention(values['content'])
            # if self.do_mentions:
            #     self.do_mentions(record['user_id'], POST_TYPES.TOPIC, record['id'], {
            #         'title': record['title'],
            #     })

        async def on_complete(id_lst: IDList):
            # 创建完成后添加入日志
            for id_ in id_lst:
                # TODO: 管理日志：新建板块
                # ManageLogModel.post_new(self, POST_TYPES.BOARD, record)

                if config.SEARCH_ENABLE:
                    run_in_thread(esdb.es_update_topic, id_)

        when_complete.append(on_complete)

    @classmethod
    async def on_read(
            cls,
            info: 'QueryInfo',
            when_complete: List[Callable[[List[QueryResultRow]], Awaitable]],
            perm: 'PermInfo' = None
    ):

        async def _when_complete(results: List[QueryResultRow]):
            # 记录点击数
            for i in results:
                r = i.to_dict()
                if r.get('board_id'):
                    post_stats_add_topic_click(i.id, )

        when_complete.append(_when_complete)
