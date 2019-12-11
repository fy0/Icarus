# coding:utf-8
import random
import time
from peewee import *
from model._post import POST_STATE, POST_VISIBLE, PostModel, POST_TYPES
from model.post_stats import post_stats_new
from slim.utils import StateObject, get_bytes_from_blob
from model import BaseModel, MyTimestampField, db
from model.user import User
# from model.board import Board


DEFAULT_SIDEBAR_CONTENT = '''
# 侧边栏文本
[转至主页](/)
[转至关于](/about)

# 一些计划
> 加入搜索功能
> 加入OAuth登录
'''

DEFAULT_WIKI_CONTENT = '''
# 欢迎来到Icarus百科

如你所见，所谓百科主页面就是显示在右边的页面。

实际上也就是个有点特殊的百科文档而已，和其他文档并无太大的不同。

反正这里放一些导航啊、守则啊、介绍啊之类的内容即可。
'''


class WikiArticle(PostModel):
    title = TextField(index=True)
    content = TextField()
    ref = TextField(index=True, unique=True, null=True)
    flag = IntegerField(index=True, null=True, default=None)

    class Meta:
        db_table = 'wiki_article'

    @classmethod
    def get_sidebar_article(cls):
        try:
            return cls.select().where(cls.flag == 1).get()
        except cls.DoesNotExist:
            a = cls.insert(time=int(time.time()), user_id=None, flag=1, title="侧边栏",
                           content=DEFAULT_SIDEBAR_CONTENT, ref=None).execute()
            post_stats_new(POST_TYPES.WIKI, get_bytes_from_blob(a))
            return cls.get(cls.id == a)

    @classmethod
    def get_main_page_article(cls):
        try:
            return cls.select().where(cls.flag == 2).get()
        except cls.DoesNotExist:
            a = cls.insert(time=int(time.time()), user_id=None, flag=2, title="主页面",
                           content=DEFAULT_WIKI_CONTENT, ref=None).execute()
            post_stats_new(POST_TYPES.WIKI, get_bytes_from_blob(a))
            return cls.get(cls.id == a)

    @classmethod
    def get_random_one(cls) -> bytes:
        try:
            wa = cls.select(cls.ref)\
                .where(cls.state >= POST_STATE.NORMAL, cls.flag.is_null()) \
                .order_by(fn.Random())\
                .limit(1) \
                .get()
            # return wa.id.tobytes()
            return wa.ref
        except cls.DoesNotExist:
            pass

    @classmethod
    def get_post_type(cls):
        return POST_TYPES.WIKI

    def get_title(self):
        return self.title
