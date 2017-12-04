import time
import config
from typing import Dict

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

    def handle_insert(self, values: Dict):
        relate_type = values.get('related_type', None)
        if not (relate_type and relate_type.isdigit() and int(relate_type) in POST_TYPES.values()):
            return self.finish(RETCODE.INVALID_HTTP_POSTDATA, "被评论的内容不存在")

        try:
            cid = CustomID(values['related_id'])
            post = POST_TYPES.get_post(relate_type, cid)

            if not post:
                return self.finish(RETCODE.INVALID_HTTP_POSTDATA, "被评论的内容不存在")
        except TypeError:
            return self.finish(RETCODE.INVALID_HTTP_POSTDATA, "被评论的内容不存在")

        if 'content' not in values or not values['content']:
            return self.finish(RETCODE.INVALID_HTTP_POSTDATA, "评论内容不能为空")

        values['id'] = CustomID().to_bin()
        values['related_type'] = int(values['related_type'])
        values['user_id'] = self.current_user
        values['time'] = int(time.time())
