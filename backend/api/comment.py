import time
import config
from typing import Dict, List

from app import app
from model import esdb
from model.manage_log import ManageLog, MANAGE_OPERATION as MOP
from model.post_stats import post_stats_do_comment
from model.topic import Topic
from slim.base.permission import Permissions
from slim.base.sqlquery import SQLValuesToWrite, DataRecord
from slim.utils.customid import CustomID
from model.comment import Comment
from model._post import POST_TYPES, POST_STATE, POST_VISIBLE
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin, get_bytes_from_blob
from api import ValidateForm, cooldown, same_user, run_in_thread
from wtforms import validators as va, StringField, IntegerField, ValidationError
from api.mention import check_content_mention
from api.user import UserViewMixin


@app.route.view('comment')
class CommentView(UserViewMixin, PeeweeView):
    model = Comment

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('reply_to_cmt_id', 'comment')

    @cooldown(config.COMMENT_NEW_COOLDOWN_BY_IP, b'ic_cd_comment_new_%b')
    @cooldown(config.COMMENT_NEW_COOLDOWN_BY_ACCOUNT, b'ic_cd_comment_new_account_%b', unique_id_func=same_user)
    async def new(self):
        return await super().new()

    async def prepare(self):
        self.do_mentions = None

    async def before_insert(self, values_lst: List[SQLValuesToWrite]):
        for values in values_lst:
            relate_type = values.get('related_type', None)
            if not (relate_type and relate_type in POST_TYPES.values()):
                return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

            try:
                cid = config.POST_ID_GENERATOR(values['related_id'])
                post = POST_TYPES.get_post(relate_type, cid)

                if not post:
                    return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

                if relate_type == POST_TYPES.TOPIC:
                    if post.state == POST_STATE.CLOSE:
                        return self.finish(RETCODE.INVALID_POSTDATA, "无法评论指定内容")
                    elif post.visible in (POST_VISIBLE.HIDE,):
                        return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

            except TypeError:
                return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

            if 'content' not in values or not values['content']:
                return self.finish(RETCODE.INVALID_POSTDATA, "评论内容不能为空")

            if 'reply_to_cmt_id' in values:
                try:
                    rtid = config.POST_ID_GENERATOR(values['reply_to_cmt_id'])
                except TypeError:
                    return self.finish(RETCODE.INVALID_POSTDATA, "指定被回复的内容不存在")
                c: Comment = Comment.get_by_pk(rtid.to_bin())

                if not c:
                    return self.finish(RETCODE.INVALID_POSTDATA, "指定被回复的内容不存在")
                if c.related_id != post.id:
                    return self.finish(RETCODE.INVALID_POSTDATA, "指定被回复的内容不存在")

                values['reply_to_cmt_id'] = rtid.to_bin()

            if not isinstance(config.LONG_ID_GENERATOR, config.SQLSerialGenerator):
                values['id'] = config.LONG_ID_GENERATOR().to_bin()
            values['related_id'] = cid.to_bin()
            values['related_type'] = int(values['related_type'])
            values['user_id'] = self.current_user.id
            values['time'] = int(time.time())
            values['content'], self.do_mentions = check_content_mention(values['content'])

            if relate_type == POST_TYPES.TOPIC:
                post: Topic
                await post.weight_inc()

    async def after_insert(self, values_lst: List[SQLValuesToWrite], records: List[DataRecord]):
        for record in records:
            post_stats_do_comment(record['related_type'], record['related_id'], record['id'])
            post_number = Comment.select().where(Comment.related_id == record['related_id'], Comment.id <= record['id']).count()
            Comment.update(post_number=post_number).where(Comment.id == record['id']).execute()

            if self.do_mentions:
                # 创建提醒
                loc = [record['related_type'], record['related_id']]
                # record['related_id']: memoryview
                loc_title = POST_TYPES.get_post_title_by_list(loc)[get_bytes_from_blob(record['related_id'])]
                related = [POST_TYPES.COMMENT, record['id']]
                self.do_mentions(record['user_id'], loc_title, loc, related)

            if config.SEARCH_ENABLE:
                run_in_thread(esdb.es_update_comment, record['id'])

    async def after_update(self, values: SQLValuesToWrite, old_records: List[DataRecord],
                           new_records: List[DataRecord]):
        for old_record, record in zip(old_records, new_records):
            # 管理日志：修改评论状态
            ManageLog.add_by_post_changed(self, 'state', MOP.POST_STATE_CHANGE, POST_TYPES.COMMENT,
                                          values, old_record, record)

            if config.SEARCH_ENABLE:
                run_in_thread(esdb.es_update_comment, record['id'])
