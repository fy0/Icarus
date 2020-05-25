# coding:utf-8

"""
一些通用类的定义
"""
import time
from abc import abstractmethod
from typing import Dict, Type, Optional

from peewee import *

import config
from slim.base.sqlquery import DataRecord

from config import POST_ID_GENERATOR
from slim.utils import get_bytes_from_blob
from slim.utils.customid import CustomID
from slim.utils.state_obj import StateObject
from model import BaseModel, MyTimestampField


class POST_STATE(StateObject):
    DEL = 0
    APPLY = 20  # 等待发布审核
    CLOSE = 30  # 禁止回复
    NORMAL = 50

    txt = {DEL: "删除", APPLY: '待审核', CLOSE: "锁定", NORMAL: "正常"}


class POST_VISIBLE(StateObject):
    HIDE = 10
    PRIVATE = 30
    NOT_IN_LIST = 40
    NORMAL = 50
    CONTENT_IF_LOGIN = 60
    USER_ONLY = 70
    ADMIN_ONLY = 80

    txt = {HIDE: "隐藏", PRIVATE: '仅个人可见', NOT_IN_LIST: '不在列表中', NORMAL: "标准",
           CONTENT_IF_LOGIN: '登陆后可见正文', USER_ONLY: '仅会员可见', ADMIN_ONLY: '仅管理员可见'}


class POST_TYPES(StateObject):
    NONE    =  0
    USER    = 10
    BOARD   = 20
    TOPIC   = 30
    WIKI    = 40
    COMMENT = 50
    MENTION = 60
    UPLOAD  = 70

    txt = {NONE: "???", USER:"用户", BOARD: '板块', TOPIC: '主题', WIKI: '百科', COMMENT: '评论', MENTION: '召唤',
           UPLOAD: '上传'}

    TITLE_FIELD = {
        USER: 'nickname',
        BOARD: 'name',
        TOPIC: 'title',
        WIKI: 'title',
        COMMENT: None,
        MENTION: None,
        UPLOAD: None
    }

    @classmethod
    def get_model(cls, related_type) -> Type['PostModel']:
        from model.user import User
        from model.topic import Topic
        from model.comment import Comment
        from model.board import Board
        from model.wiki import WikiArticle
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
            return WikiArticle

    @classmethod
    def get_post(cls, related_type, related_id) -> Optional['PostModel']:
        from model.user import User
        from model.topic import Topic
        from model.wiki import WikiArticle

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
            fields = [m._meta.primary_key,]

            # 获取标题列
            title_field = cls.TITLE_FIELD.get(related_type)
            if title_field:
                fields.append(getattr(m, title_field))

            # 按分类分别执行查询
            for i in m.select(*fields).where(m.id.in_(id_lst)):
                ret[get_bytes_from_blob(i.id)] = i.get_title()

        return ret


def get_time():
    return int(time.time())


class PostModel(BaseModel):
    id = BlobField(primary_key=True, constraints=[SQL("DEFAULT int2bytea(nextval('id_gen_seq'))")])
    state = IntegerField(default=POST_STATE.NORMAL, index=True)
    visible = IntegerField(default=POST_VISIBLE.NORMAL, index=True)
    time = MyTimestampField(index=True, default=get_time, help_text='发布时间')
    user_id = BlobField(index=True, null=True, default=None)  # 发布用户，对 user 表来说是推荐者，对 board 来说是创建者

    # is_for_tests = BooleanField(default=False, help_text='单元测试标记，单元测试结束后删除')

    @classmethod
    @abstractmethod
    def get_post_type(cls):
        """
        获取类型ID
        :return:
        """
        pass

    @abstractmethod
    def get_title(self):
        pass

    @classmethod
    def append_post_id(cls, values):
        """
        若有ID生成器，那么向values中添加生成出的值，若生成器为SQL Serial，则什么都不做
        :param values:
        :return:
        """
        if config.POST_ID_GENERATOR != config.SQLSerialGenerator:
            values['id'] = config.POST_ID_GENERATOR().to_bin()


def get_model_id():
    return config.LONG_ID_GENERATOR().to_bin()


class LongIdPostModel(PostModel):
    id = BlobField(primary_key=True, default=get_model_id)

    def get_title(self):
        """
        大部分情况下 LongIdPostModel 都没有标题
        :return:
        """
        return None

    @classmethod
    def append_post_id(cls, values):
        """
        若有ID生成器，那么向values中添加生成出的值，若生成器为SQL Serial，则什么都不做
        :param values:
        :return:
        """
        if config.LONG_ID_GENERATOR != config.SQLSerialGenerator:
            values['id'] = config.LONG_ID_GENERATOR().to_bin()


def get_title_by_record(post_type, record: DataRecord):
    """
    根据返回的 record 来获取title
    :param post_type:
    :param record:
    :return:
    """
    tfield = POST_TYPES.TITLE_FIELD[post_type]
    return record.get(tfield) if tfield else None
