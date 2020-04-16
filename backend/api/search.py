from app import app
from model import esdb
from model._post import POST_VISIBLE
from slim.retcode import RETCODE

import config
from slim.base.view import BaseView
from api import cooldown, thread_executor, run_in_thread
from api.user import UserViewMixin


@app.route.view('search')
class TestBaseView(UserViewMixin, BaseView):
    @app.route.interface('POST')
    @cooldown(config.SEARCH_COOLDOWN_BY_IP, b'ic_cd_search_cooldown_by_ip_%b')
    async def search(self):
        post = await self.post_data()
        vmax = POST_VISIBLE.CONTENT_IF_LOGIN
        role = list(self.roles)[-1]
        if role in ('forum_master', 'superuser', 'admin'):
            vmax = POST_VISIBLE.ADMIN_ONLY
        ret = await run_in_thread(esdb.doc_search, post['keywords'], visible_max=vmax)
        self.finish(RETCODE.SUCCESS, ret.to_dict())
