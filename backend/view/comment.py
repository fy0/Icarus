import time
import config
from typing import Dict

from model.statistic import statistic_add_comment
from model.topic import Topic, TOPIC_STATE
from slim.utils.customid import CustomID
from model.comment import Comment
from model.post import POST_TYPES
from slim.base.view import ParamsQueryInfo
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin
from view import route, ValidateForm
from wtforms import validators as va, StringField, IntegerField, ValidationError
from view.user import UserMixin


@route('comment')
class CommentView(UserMixin, PeeweeView):
    model = Comment

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('reply_to_cmt_id', 'comment')

    def before_insert(self, raw_post: Dict, values: Dict):
        relate_type = values.get('related_type', None)
        if not (relate_type and relate_type.isdigit() and int(relate_type) in POST_TYPES.values()):
            return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

        try:
            relate_type = int(relate_type)
            cid = config.ID_GENERATOR(values['related_id'])
            post = POST_TYPES.get_post(relate_type, cid)

            if not post:
                return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

            if relate_type == POST_TYPES.TOPIC:
                if post.state == TOPIC_STATE.CLOSE:
                    return self.finish(RETCODE.INVALID_POSTDATA, "无法评论指定内容")
                elif post.state in (TOPIC_STATE.HIDE, TOPIC_STATE.CLOSE):
                    return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

        except TypeError:
            return self.finish(RETCODE.INVALID_POSTDATA, "被评论的内容不存在")

        if 'content' not in values or not values['content']:
            return self.finish(RETCODE.INVALID_POSTDATA, "评论内容不能为空")

        if 'reply_to_cmt_id' in values:
            try:
                rtid = config.ID_GENERATOR(values['reply_to_cmt_id'])
            except TypeError:
                return self.finish(RETCODE.INVALID_POSTDATA, "指定被回复的内容不存在")
            c: Comment = Comment.get_by_pk(rtid.to_bin())
            if not c:
                return self.finish(RETCODE.INVALID_POSTDATA, "指定被回复的内容不存在")
            if c.related_id != post.id:
                return self.finish(RETCODE.INVALID_POSTDATA, "指定被回复的内容不存在")

            values['reply_to_cmt_id'] = rtid.to_bin()

        values['id'] = config.ID_GENERATOR().to_bin()
        values['related_id'] = cid.to_bin()
        values['related_type'] = int(values['related_type'])
        values['user_id'] = self.current_user.id
        values['time'] = int(time.time())

        if relate_type == POST_TYPES.TOPIC:
            post: Topic
            post.weight_inc()

    def after_insert(self, values: Dict):
        statistic_add_comment(values['related_type'], values['related_id'], values['id'])
