from api.view.curd import BaseCrudUserView
from app import app
import config
from typing import Dict

from crud.schemas.notif import Notification
from model.notif import NotificationModel
from slim.ext.decorator import timer
from slim.retcode import RETCODE


@app.route.view('notif')
class NotificationView(BaseCrudUserView):
    model = Notification

    # @classmethod
    # def interface_register(cls):
    #     cls.unregister('new')
    #     cls.unregister('set')
    #     cls.unregister('delete')

    @classmethod
    def ready(cls):
        # cls.add_soft_foreign_key('user_id', 'user')
        # cls.add_soft_foreign_key('reply_to_cmt_id', 'comment')
        pass

    @app.route.interface('POST')
    async def set_read(self):
        if self.current_user:
            c = NotificationModel.set_read(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)

    @app.route.interface('GET')
    async def count(self):
        if self.current_user:
            c = NotificationModel.count(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)

    @app.route.interface('POST')
    async def refresh(self):
        """
        由 misc/tick 替代，此方法弃用
        :return:
        """
        if self.current_user:
            r = NotificationModel.refresh(self.current_user.id)
            c = NotificationModel.count(self.current_user.id)
            return self.finish(RETCODE.SUCCESS, c)
        self.finish(RETCODE.FAILED)


'''
@timer(config.NOTIF_FETCH_COOLDOWN + 1, exit_when=None)
async def notif_refresh():
    for user, conns in WSR.users.items():
        r = NotificationModel.refresh(user.id)
        c = NotificationModel.count(user.id)

        for ws in conns:
            if not ws.closed:
                await ws.send_json(['notif.refresh', c])
'''

