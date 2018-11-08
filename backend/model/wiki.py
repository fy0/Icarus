# coding:utf-8
import random
import time
from peewee import *
from model._post import POST_STATE, POST_VISIBLE, PostModel, POST_TYPES
from model.post_stats import post_stats_new
from slim.utils import StateObject
from model import BaseModel, MyTimestampField, db
from model.user import User
# from model.board import Board


class WikiArticle(PostModel):
    title = TextField(index=True)
    content = TextField()
    ref = TextField(index=True, unique=True, null=True)
    flag = IntegerField(index=True, null=True, default=None)

    class Meta:
        db_table = 'wiki_article'

    def get_title(self):
        return self.title

    @classmethod
    def get_sidebar_article(cls):
        try:
            return cls.select().where(cls.flag == 1).get()
        except cls.DoesNotExist:
            a = cls.insert(time=int(time.time()), user_id=None, flag=1, title="侧边栏",
                           content='侧边栏文本', link=None).execute()
            post_stats_new(POST_TYPES.WIKI, a.tobytes())
            return cls.get(cls.id == a)

    @classmethod
    def get_main_page_article(cls):
        try:
            return cls.select().where(cls.flag == 2).get()
        except cls.DoesNotExist:
            a = cls.insert(time=int(time.time()), user_id=None, flag=2, title="主页面",
                           content='主页面文本', link=None).execute()
            post_stats_new(POST_TYPES.WIKI, a.tobytes())
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
