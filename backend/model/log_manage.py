import time
from peewee import *
from playhouse.postgres_ext import BinaryJSONField
from slim.base.sqlquery import DataRecord

import config
from model import BaseModel, MyTimestampField
from model._post import POST_TYPES
from slim import json_ex_dumps
from slim.utils import StateObject


class MANAGE_OPERATION(StateObject):
    POST_STATE_CHANGE = 0  # 改变状态：例如删除等等
    POST_VISIBLE_CHANGE = 1

    USER_PASSWORD_CHANGE = 100  # 设置用户密码（未来再做区分，现在仅有这个）
    USER_PASSWORD_RESET = 101  # 重置用户密码
    USER_KEY_RESET = 102
    USER_GROUP_CHANGE = 103
    USER_CREDIT_CHANGE = 104
    USER_REPUTE_CHANGE = 105
    USER_EXP_CHANGE = 106
    USER_NICKNAME_CHANGE = 107

    BOARD_NEW = 200
    BOARD_CHANGE = 201

    TOPIC_TITLE_CHANGE = 300  # 修改标题
    TOPIC_CONTENT_CHANGE = 301  # 修改主题
    TOPIC_BOARD_MOVE = 302  # 移动主题到其他板块
    TOPIC_AWESOME_CHANGE = 303
    TOPIC_STICKY_WEIGHT_CHANGE = 305
    TOPIC_WEIGHT_CHANGE = 306

    COMMENT_STATE_CHANGE = 500  # 修改评论状态

    txt = {
        POST_STATE_CHANGE: '改变状态',
        POST_VISIBLE_CHANGE: '修改可见度',

        USER_PASSWORD_CHANGE: '重设用户密码',
        USER_PASSWORD_RESET: '重置用户密码',
        USER_KEY_RESET: "重置用户访问令牌",
        USER_GROUP_CHANGE: '修改用户组',
        USER_CREDIT_CHANGE: '积分变更',
        USER_REPUTE_CHANGE: "声望变更",
        USER_EXP_CHANGE: "经验值变更",

        BOARD_NEW: '新建板块',
        BOARD_CHANGE: '修改板块信息',

        TOPIC_TITLE_CHANGE: '修改标题',
        TOPIC_CONTENT_CHANGE: '编辑内容',
        TOPIC_BOARD_MOVE: '移动',
        TOPIC_AWESOME_CHANGE: '设置优秀文章',
        TOPIC_STICKY_WEIGHT_CHANGE: '修改置顶权重',
        TOPIC_WEIGHT_CHANGE: '修改板块权重',

        COMMENT_STATE_CHANGE: '修改评论状态',
    }


class ManageLog(BaseModel):
    id = BlobField(primary_key=True)  # 使用长ID
    user_id = BlobField(index=True, null=True)  # 操作用户
    role = TextField(null=True)  # 操作身份
    time = MyTimestampField(index=True)  # 操作时间
    related_type = IntegerField()  # 被操作对象类型
    related_id = BlobField(index=True)  # 被操作对象
    related_user_id = BlobField(index=True, null=True)  # 附加关联对象涉及用户
    operation = IntegerField()  # 操作行为
    value = BinaryJSONField(dumps=json_ex_dumps, null=True)  # 操作数据
    note = TextField(null=True, default=None)

    @classmethod
    def new(cls, user_id, role, related_type, related_id, related_user_id, operation, value, note=None):
        return cls.create(
            id=config.LONG_ID_GENERATOR().digest(),
            user_id=user_id,
            role=role,
            time=int(time.time()),
            related_type=related_type,
            related_id=related_id,
            related_user_id=related_user_id,
            operation=operation,
            value=value,
            note=note
        )

    @classmethod
    def add_by_credit_changed(cls, view, changed_user, note=None, *, value=None):
        if view:
            user_id = view.current_user.id
            role = view.current_role
        else:
            user_id = None
            role = None

        return cls.new(user_id, role, POST_TYPES.USER, changed_user.id, changed_user.id,
                       MANAGE_OPERATION.USER_CREDIT_CHANGE, value, note=note)

    @classmethod
    def add_by_credit_changed_sys(cls, changed_user, note=None, *, value=None):
        return cls.add_by_credit_changed(None, changed_user, note, value=value)

    @classmethod
    def add_by_repute_changed(cls, view, changed_user, note=None, *, value=None):
        if view:
            user_id = view.current_user.id
            role = view.current_role
        else:
            user_id = None
            role = None

        return cls.new(user_id, role, POST_TYPES.USER, changed_user.id, changed_user.id,
                       MANAGE_OPERATION.USER_REPUTE_CHANGE, value, note=note)

    @classmethod
    def add_by_repute_changed_sys(cls, changed_user, note=None, *, value=None):
        return cls.add_by_repute_changed(None, changed_user, note, value=value)

    @classmethod
    def add_by_exp_changed(cls, view, changed_user, note=None, *, value=None):
        if view:
            user_id = view.current_user.id
            role = view.current_role
        else:
            user_id = None
            role = None

        return cls.new(user_id, role, POST_TYPES.USER, changed_user.id, changed_user.id,
                       MANAGE_OPERATION.USER_EXP_CHANGE, value, note=note)

    @classmethod
    def add_by_exp_changed_sys(cls, changed_user, note=None, *, value=None):
        return cls.add_by_exp_changed(None, changed_user, note, value=value)

    @classmethod
    def add_by_post_changed(cls, view, key, operation, related_type, values, old_record, record, note=None,
                            *, value=NotImplemented):
        def get_val(r, k):
            if isinstance(r, (DataRecord, dict)):
                return r[k]
            elif isinstance(r, BaseModel):
                return getattr(r, k)
            else:
                raise TypeError()

        def key_in_values():
            if isinstance(values, dict):
                return key in values
            elif isinstance(values, bool):
                return values
            else:
                raise TypeError()

        if key_in_values():
            if value is NotImplemented:
                value = [get_val(old_record, key), get_val(record, key)]

            return cls.new(view.current_user.id, view.current_role, related_type, get_val(record, 'id'),
                           get_val(record, 'user_id'), operation, value, note=note)

    class Meta:
        db_table = 'manage_log'
