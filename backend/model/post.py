# coding:utf-8

"""
一些通用类的定义
"""

from peewee import *
from config import POST_ID_GENERATOR
from slim.utils.customid import CustomID
from slim.utils.state_obj import StateObject
from model import BaseModel


class POST_STATE(StateObject):
    DEL = 0
    INACTIVE = 10 # 未激活
    APPLY = 20  # 等待发布审核
    CLOSE = 30  # 禁止回复
    NORMAL = 50

    txt = {DEL: "删除", INACTIVE: '未激活', APPLY: '待审核', CLOSE: "关闭", NORMAL: "正常"}


class POST_VISIBLE(StateObject):
    HIDE = 10
    NORMAL = 50
    CONTENT_IF_LOGIN = 60
    USER_ONLY = 70
    ADMIN_ONLY = 80

    txt = {HIDE: "隐藏", NORMAL:"标准", CONTENT_IF_LOGIN: '登陆后可见正文', USER_ONLY: '仅会员可见', ADMIN_ONLY: '仅管理员可见'}


class POST_TYPES(StateObject):
    NONE    =  0
    USER    = 10
    BOARD   = 20
    TOPIC   = 30
    WIKI    = 40
    COMMENT = 50

    @classmethod
    def get_post(cls, related_type, related_id):
        from model.user import User
        from model.topic import Topic
        from model.wiki import WikiItem

        if type(related_id) == POST_ID_GENERATOR:
            related_id = related_id.to_bin()

        if type(related_type) == str:
            related_type = int(related_type)

        if related_type == POST_TYPES.USER:
            u = User.get_by_pk(related_id)
            if u: return u
        elif related_type == POST_TYPES.TOPIC:
            t = Topic.get_by_pk(related_id)
            if t: return t
        elif related_type == POST_TYPES.WIKI:
            w = WikiItem.get_by_pk(related_id)
            if w: return w
