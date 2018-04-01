# coding:utf-8
import random
import time
from peewee import *

from model.post import POST_STATE, POST_VISIBLE
from slim.utils import StateObject
from model import BaseModel, MyTimestampField
from model.user import User
# from model.board import Board


'''
关于百科版本号的说明：
百科的版本管理主要涉及词条（WikiItem）、文章（WikiArticle）、版本历史（WikiHistory）三个类
首先创建词条，随后针对词条撰写内容，第一篇文章的主版本号是0，小版本号是1，这时进入待审核状态
当审核通过之后，将其录入至版本历史，同时词条版本号加一，成为第一版

之后对第一版提出修改的人会基于第一版拥有自己的版本，假设ABC三人同时申请修改
那么按照时间先后顺序，他们三人依次拥有 1.1 1.2 1.3 三个版本，但此时词条仍会显示原始的1.0版本
随后A弃坑，BC两人分别把自己的改动交与审核。管理员发现B对词条进行了比较好的完善，但C改的很烂，于是选择了B的版本
于是B的1.2版本升格为词条的第二版，即2.0版本，同时录入版本历史。
新的编辑者只能在2.0版本基础上进行修改，他们的版本又分别为 2.1 2.2 2.3 ...
'''


class WikiArticle(BaseModel):
    id = BlobField(primary_key=True)
    user_id = BlobField(index=True)
    time = MyTimestampField(index=True)
    state = IntegerField(default=POST_STATE.APPLY, index=True)
    visible = IntegerField(default=POST_VISIBLE.NORMAL, index=True)

    major_ver = IntegerField()
    minor_ver = IntegerField()

    parent = IntegerField(index=True, null=True)  # wiki article
    root = IntegerField(index=True)  # wiki item

    content = TextField()

    class Meta:
        db_table = 'wiki_article'


class WikiItem(BaseModel):
    id = BlobField(primary_key=True)
    title = CharField(index=True, unique=True, max_length=50)
    keyword = CharField(index=True, unique=True, max_length=20)
    current = ForeignKeyField(WikiArticle, index=True, null=True)
    time = BigIntegerField(index=True)
    version = IntegerField(default=0)

    class Meta:
        db_table = 'wiki_item'


class WikiHistory(BaseModel):
    id = BlobField(primary_key=True)
    wiki = ForeignKeyField(WikiItem, index=True)
    item = ForeignKeyField(WikiArticle, index=True)
    major_ver = IntegerField()

    class Meta:
        db_table = 'wiki_history'
