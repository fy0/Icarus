import time
import config
from typing import Dict
from model.notif import Notification
from model.statistic import statistic_add_comment
from model.topic import Topic
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


@route('notif')
class NotificationView(UserMixin, PeeweeView):
    model = Notification

    @classmethod
    def interface(cls):
        super().interface()
        cls.discard('new')
        cls.discard('set')
        cls.discard('delete')

    @classmethod
    def ready(cls):
        # cls.add_soft_foreign_key('user_id', 'user')
        # cls.add_soft_foreign_key('reply_to_cmt_id', 'comment')
        pass

    @route.interface('POST')
    async def set_read(self):
        if self.current_user:
            c = self.model.set_read(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)

    @route.interface('GET')
    async def count(self):
        if self.current_user:
            c = self.model.count(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)

    @route.interface('POST')
    async def refresh(self):
        if self.current_user:
            r = self.model.refresh(self.current_user.id)
            c = self.model.count(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)
