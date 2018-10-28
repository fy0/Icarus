# coding:utf-8
import random
import time
from peewee import *
from model._post import POST_STATE, POST_VISIBLE, PostModel, POST_TYPES
from model.statistic import statistic_new
from slim.utils import StateObject
from model import BaseModel, MyTimestampField
from model.user import User

# from model.board import Board


'''
关于百科版本号的说明：
百科的最小单位是文章（WikiArticle），使用一个简单的版本管理机制。
有点像是程序的版本库，初始的文章主版本号为1，而基于初始版本更新的文章则不断进行主版本号+1。
副版本号用于表示草稿，换句话说，只有副版本号为零的最新一个主版本才是文章的当前版本。

举个例子，创建一篇百科文章，主版本号1，这是第一版。
之后对第一版提出修改的人会基于第一版拥有自己的版本，假设ABC三人申请修改此文章
那么按照时间先后顺序，他们三人依次拥有 1.1 1.2 1.3 三个版本，但此时词条仍会显示原始的1.0版本
当三人改动完成之后，管理员认为B的改动较为完善，于是选择B的改动为下一版。
于是B的1.2版本升格为词条的第二版，即2.0版本，其他人改动作废。
新的编辑者又只能在2.0版本基础上进行修改，他们的版本又分别为 2.1 2.2 2.3 ...
'''


class WikiArticle(PostModel):
    title = TextField(index=True)
    root_id = BlobField(index=True, null=True)  # 新文章的root是null，后续继承者继承其父级的root
    parent_id = BlobField(index=True, null=True)
    content = TextField()
    # link_name = TextField(index=Tree)

    flag = IntegerField(index=True, null=True, default=None)
    is_current = BooleanField(index=True, default=False)
    major_ver = IntegerField(index=True)
    minor_ver = IntegerField()

    class Meta:
        db_table = 'wiki_article'

    def get_title(self):
        return self.title

    @classmethod
    def get_sidebar_root_article(cls):
        try:
            return cls.select().where(cls.flag == 1, cls.root_id.is_null()).get()
        except cls.DoesNotExist:
            a = cls.insert(time=int(time.time()), user_id=None, flag=1, is_current=True,
                           major_ver=1, minor_ver=0, title="侧边栏", content='侧边栏文本').execute()
            statistic_new(POST_TYPES.WIKI, a.tobytes())
            return cls.get(cls.id == a)

    @classmethod
    def get_main_page_root_article(cls):
        try:
            return cls.select().where(cls.flag == 2, cls.root_id.is_null()).get()
        except cls.DoesNotExist:
            a = cls.insert(time=int(time.time()), user_id=None, flag=2, is_current=True,
                           major_ver=1, minor_ver=0, title="主页面", content='主页面文本').execute()
            statistic_new(POST_TYPES.WIKI, a.tobytes())
            return cls.get(cls.id == a)
