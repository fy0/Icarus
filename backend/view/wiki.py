import time
from urllib.parse import quote
from typing import Dict, List
from peewee import fn
import config
from lib.textdiff import diff
from model._post import POST_TYPES
from model.manage_log import ManageLog, MANAGE_OPERATION as MOP
from model.post_stats import post_stats_new, post_stats_incr, PostStats, post_stats_do_edit
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


class WikiEditForm(ValidateForm):
    title = StringField('标题', validators=[
        va.optional(),
        va.Length(config.POST_TITLE_LENGTH_MIN, config.POST_TITLE_LENGTH_MAX)
    ])

    content = StringField('正文', validators=[
        va.optional(),
        va.Length(1, config.POST_CONTENT_LENGTH_MAX)
    ])

    # ref = StringField('地址', validators=[
    #     va.required(),
    # ])


@route('wiki')
class WikiView(UserMixin, PeeweeView):
    """
    文档有一个简单的版本设定，但忽略任何并发导致的同步问题
    """
    model = WikiArticle

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'post_stats', alias='s')
        cls.add_soft_foreign_key('user_id', 'user')

    @classmethod
    def permission_init(cls):
        permission: Permissions = cls.permission
        permissions_add_all(permission)

    @route.interface('GET')
    async def random(self):
        wa = WikiArticle.get_random_one()
        if wa:
            self.finish(RETCODE.SUCCESS, {'ref': wa})
        else:
            self.finish(RETCODE.NOT_FOUND)

    def after_read(self, records: List[DataRecord]):
        for i in records:
            self._val_bak = i['id']

    async def get(self):
        await super().get()
        if self.ret_val['code'] == RETCODE.SUCCESS:
            post_stats_incr(PostStats.click_count, self._val_bak)
            val = getattr(self, '_val_bak', None)
            if val: post_stats_incr(PostStats.click_count, val)

    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_IP, b'ic_cd_wiki_new_%b', cd_if_unsuccessed=10)
    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_ACCOUNT, b'ic_cd_wiki_new_account_%b', unique_id_func=same_user, cd_if_unsuccessed=10)
    async def new(self):
        return await super().new()

    async def before_update(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]
        form = WikiEditForm(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

    def after_update(self, raw_post: Dict, values: SQLValuesToWrite, old_records: List[DataRecord], records: List[DataRecord]):
        for old_record, record in zip(old_records, records):
            manage_try_add = lambda column, op: ManageLog.add_by_post_changed(
                self, column, op, POST_TYPES.WIKI, values, old_record, record
            )
            manage_try_add_with_diff = lambda column, op: ManageLog.add_by_post_changed(
                self, column, op, POST_TYPES.WIKI, values, old_record, record, diff_func=diff
            )

            title_changed = manage_try_add('title', MOP.POST_TITLE_CHANGE)  # 管理日志：标题编辑
            content_changed = manage_try_add_with_diff('content', MOP.POST_CONTENT_CHANGE)  # 管理日志：正文编辑

            if title_changed or content_changed:
                post_stats_do_edit(record['id'], record['user_id'])

            manage_try_add('ref', MOP.WIKI_REF_CHANGE)  # 管理日志：链接编辑
            manage_try_add('state', MOP.POST_STATE_CHANGE)  # 管理日志：改变状态
            manage_try_add('visible', MOP.POST_VISIBLE_CHANGE)  # 管理日志：改变可见度

    async def before_insert(self, raw_post: Dict, values_lst: List[SQLValuesToWrite]):
        values = values_lst[0]
        form = WikiNewForm(**raw_post)
        if not form.validate():
            return self.finish(RETCODE.FAILED, form.errors)

        values['time'] = int(time.time())
        values['user_id'] = self.current_user.id

        ref = values.get('ref', '').strip()
        if not ref: ref = values['title']
        values['ref'] = quote(ref).replace('/', '')

    def after_insert(self, raw_post: Dict, values: SQLValuesToWrite, records: List[DataRecord]):
        record = records[0]
        # 添加统计记录
        post_stats_new(POST_TYPES.WIKI, record['id'])
        # 添加创建记录
        ManageLog.new(self.current_user, self.current_role, POST_TYPES.WIKI, record['id'],
                      record['user_id'], MOP.POST_CREATE, record['name'])
