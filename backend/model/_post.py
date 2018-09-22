# coding:utf-8

"""
一些通用类的定义
"""
from abc import abstractmethod
from typing import Dict, Type

from peewee import *
from config import POST_ID_GENERATOR
from slim.utils.customid import CustomID
from slim.utils.state_obj import StateObject
from model import BaseModel, MyTimestampField


class POST_STATE(StateObject):
    DEL = 0
    APPLY = 20  # 等待发布审核
    CLOSE = 30  # 禁止回复
    NORMAL = 50

    txt = {DEL: "删除", APPLY: '待审核', CLOSE: "关闭", NORMAL: "正常"}


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
    MENTION = 60

    txt = {NONE: "???", USER:"用户", BOARD: '板块', TOPIC: '主题', WIKI: '百科', COMMENT: '评论', MENTION: '召唤'}

    @classmethod
    def get_model(cls, related_type) -> Type['PostModel']:
        from model.user import User
        from model.topic import Topic
        from model.comment import Comment
        from model.board import Board
        from model.wiki import WikiItem
        from model.mention import Mention

        if isinstance(related_type, str):
            related_type = int(related_type)

        if related_type == POST_TYPES.USER:
            return User
        elif related_type == POST_TYPES.TOPIC:
            return Topic
        elif related_type == POST_TYPES.COMMENT:
            return Comment
        elif related_type == POST_TYPES.BOARD:
            return Board
        elif related_type == POST_TYPES.MENTION:
            return Mention
        elif related_type == POST_TYPES.WIKI:
            return WikiItem

    @classmethod
    def get_post(cls, related_type, related_id):
        from model.user import User
        from model.topic import Topic
        from model.wiki import WikiItem

        if type(related_id) == POST_ID_GENERATOR:
            related_id = related_id.to_bin()

        m = cls.get_model(related_type)
        r = m.get_by_pk(related_id)
        if r: return r

    @classmethod
    def get_post_title_by_list(cls, *lst) -> Dict[bytes, str]:
        """
        :param lst: [[related_type, related_id], ...]
        :return:
        """
        ret = {}
        info = {}
        for related_type, related_id in lst:
            info.setdefault(related_type, [])
            info[related_type].append(related_id)

        for related_type, id_lst in info.items():
            m = cls.get_model(related_type)
            # 减少取值，优化性能
            fields = [m._meta.primary_key]
            if getattr(m, 'name', None):
                fields.append(getattr(m, 'name'))
            if getattr(m, 'title', None):
                fields.append(getattr(m, 'title'))
            if getattr(m, 'nickname', None):
                fields.append(getattr(m, 'nickname'))
            # 执行查询
            for i in m.select(*fields).where(m.id.in_(id_lst)):
                ret[i.id.tobytes()] = i.get_title()

        return ret


class PostModel(BaseModel):
    id = BlobField(primary_key=True, constraints=[SQL("DEFAULT int2bytea(nextval('id_gen_seq'))")])
    state = IntegerField(default=POST_STATE.NORMAL, index=True)
    visible = IntegerField(default=POST_VISIBLE.NORMAL, index=True)
    time = MyTimestampField(index=True)  # 发布时间
    user_id = BlobField(index=True, null=True, default=None)  # 发布用户，对 user 表来说是推荐者，对 board 来说是创建者

    @abstractmethod
    def get_title(self):
        pass


class LongIdPostModel(PostModel):
    id = BlobField(primary_key=True)

    def get_title(self):
        """
        大部分情况下 LongIdPostModel 都没有标题
        :return:
        """
        return None
