from app import app
import config
from typing import Dict
from model.notif import Notification
from model.post_stats import post_stats_do_comment
from model.topic import Topic
from slim.base.ws import WSRouter
from slim.ext.decorator import timer
from slim.utils.customid import CustomID
from model.comment import Comment
from model._post import POST_TYPES
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from slim.utils import to_bin, sync_call
from api import ValidateForm
from wtforms import validators as va, StringField, IntegerField, ValidationError
from api.user import UserViewMixin
# from api.ws import WSR


@app.route.view('notif')
class NotificationView(UserViewMixin, PeeweeView):
    model = Notification

    @classmethod
    def interface_register(cls):
        super().interface_register()
        cls.unregister('new')
        cls.unregister('set')
        cls.unregister('delete')

    @classmethod
    def ready(cls):
        # cls.add_soft_foreign_key('user_id', 'user')
        # cls.add_soft_foreign_key('reply_to_cmt_id', 'comment')
        pass

    @app.route.interface('POST')
    async def set_read(self):
        if self.current_user:
            c = self.model.set_read(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)

    @app.route.interface('GET')
    async def count(self):
        if self.current_user:
            c = self.model.count(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)

    @app.route.interface('POST')
    async def refresh(self):
        """
        由 misc/tick 替代，此方法弃用
        :return:
        """
        if self.current_user:
            r = self.model.refresh(self.current_user.id)
            c = self.model.count(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)


@timer(config.NOTIF_FETCH_COOLDOWN + 1, exit_when=None)
async def notif_refresh():
    for user, conns in WSR.users.items():
        r = Notification.refresh(user.id)
        c = Notification.count(user.id)

        for ws in conns:
            if not ws.closed:
                await ws.send_json(['notif.refresh', c])
