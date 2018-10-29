import time
from typing import Dict, List

from peewee import fn

import config
from model._post import POST_TYPES
from model.log_manage import ManageLog, MANAGE_OPERATION as MOP
from model.statistic import statistic_new
from model.wiki import WikiArticle
from slim.base.permission import Permissions, DataRecord
from slim.base.sqlquery import SQLValuesToWrite
from slim.retcode import RETCODE
from slim.support.peewee import PeeweeView
from view import route, cooldown, same_user, ValidateForm
from wtforms import validators as va, StringField, IntegerField
from permissions import permissions_add_all
from view.user import UserMixin


class WikiNewForm(ValidateForm):
    title = StringField('标题', validators=[
        va.required(),
        va.Length(config.POST_TITLE_LENGTH_MIN, config.POST_TITLE_LENGTH_MAX)
    ])

    content = StringField('正文', validators=[
        va.required(),
        va.Length(1, config.POST_CONTENT_LENGTH_MAX)
    ])


@route('wiki')
class WikiView(UserMixin, PeeweeView):
    model = WikiArticle

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'statistic')
        cls.add_soft_foreign_key('user_id', 'user')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)

    @route.interface('GET')
    async def random(self):
        wa = WikiArticle.get_random_one()
        if wa:
            self.finish(RETCODE.SUCCESS, {'id': wa})
        else:
            self.finish(RETCODE.NOT_FOUND)

    async def get(self):
        await super().get()
        if self.ret_val['code'] == RETCODE.SUCCESS:
            pass

    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_IP, b'ic_cd_wiki_new_%b', cd_if_unsuccessed=10)
    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_ACCOUNT, b'ic_cd_wiki_new_account_%b', unique_id_func=same_user, cd_if_unsuccessed=10)
    async def new(self):
        return await super().new()

    def after_read(self, records: List[DataRecord]):
        for i in records:
            pass

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
        form = WikiNewForm(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        values['time'] = int(time.time())
        values['user_id'] = self.current_user.id

        # 临时选项
        values['is_current'] = True
        values['major_ver'] = 1
        values['minor_ver'] = 0
        # parent_id

    def after_insert(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]

        # 添加统计记录
        statistic_new(POST_TYPES.WIKI, record['id'])
