import time
import config
from typing import Dict, List

from model.statistic import statistic_add_comment
from model.topic import Topic
from slim.base.permission import Permissions
from slim.base.sqlquery import SQLValuesToWrite, DataRecord
from slim.utils.customid import CustomID
from model.comment import Comment
from model._post import POST_TYPES, POST_STATE, POST_VISIBLE
from slim.base.view import SQLQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin
from view import route, ValidateForm
from wtforms import validators as va, StringField, IntegerField, ValidationError

from view.permissions import visitor, normal_user, admin
from view.user import UserMixin


@route('comment')
class CommentView(UserMixin, PeeweeView):
    model = Comment

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('reply_to_cmt_id', 'comment')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permission.add(visitor)
        permission.add(normal_user)
        permission.add(admin)

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
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

        if not isinstance(config.HIDE_ID_GENERATOR, config.AutoGenerator):
            values['id'] = config.HIDE_ID_GENERATOR().to_bin()
        values['related_id'] = cid.to_bin()
        values['related_type'] = int(values['related_type'])
        values['user_id'] = self.current_user.id
        values['time'] = int(time.time())

        if relate_type == POST_TYPES.TOPIC:
            post: Topic
            post.weight_inc()

    def after_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite], records: List[DataRecord]):
        values = values_lst[0]
        statistic_add_comment(values['related_type'], values['related_id'], values['id'])
