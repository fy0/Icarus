import time
from peewee import *
from playhouse.postgres_ext import BinaryJSONField

from lib.textdiff import save_couple
from slim.base.sqlquery import DataRecord

import config
from model import BaseModel, MyTimestampField
from model._post import POST_TYPES
from slim import json_ex_dumps
from slim.utils import StateObject


class MANAGE_OPERATION(StateObject):
    POST_STATE_CHANGE = 0  # 改变状态：例如删除等等
    POST_VISIBLE_CHANGE = 1
    POST_CREATE = 2  # 被创建
    POST_TITLE_CHANGE = 3  # 修改标题
    POST_CONTENT_CHANGE = 4  # 修改内容

    USER_PASSWORD_CHANGE = 100  # 设置用户密码（未来再做区分，现在仅有这个）
    USER_PASSWORD_RESET = 101  # 重置用户密码
    USER_KEY_RESET = 102
    USER_GROUP_CHANGE = 103
    USER_CREDIT_CHANGE = 104
    USER_REPUTE_CHANGE = 105
    USER_EXP_CHANGE = 106
    USER_NICKNAME_CHANGE = 107

    BOARD_NEW = 200  # 废弃
    BOARD_CHANGE = 201

    TOPIC_BOARD_MOVE = 302  # 移动主题到其他板块
    TOPIC_AWESOME_CHANGE = 303
    TOPIC_STICKY_WEIGHT_CHANGE = 305
    TOPIC_WEIGHT_CHANGE = 306

    WIKI_REF_CHANGE = 401  # 修改链接

    # COMMENT_STATE_CHANGE = 500  # 修改评论状态

    txt = {
        POST_STATE_CHANGE: '改变状态',
        POST_VISIBLE_CHANGE: '修改可见度',
        POST_CREATE: '创建',
        POST_TITLE_CHANGE: '修改标题',
        POST_CONTENT_CHANGE: '编辑内容',

        USER_PASSWORD_CHANGE: '重设用户密码',
        USER_PASSWORD_RESET: '重置用户密码',
        USER_KEY_RESET: "重置用户访问令牌",
        USER_GROUP_CHANGE: '修改用户组',
        USER_CREDIT_CHANGE: '积分变更',
        USER_REPUTE_CHANGE: "声望变更",
        USER_EXP_CHANGE: "经验值变更",
        USER_NICKNAME_CHANGE: '昵称变更',

        BOARD_NEW: '新建板块',
        BOARD_CHANGE: '修改板块信息',

        TOPIC_BOARD_MOVE: '移动',
        TOPIC_AWESOME_CHANGE: '设置优秀文章',
        TOPIC_STICKY_WEIGHT_CHANGE: '修改置顶权重',
        TOPIC_WEIGHT_CHANGE: '修改板块权重',

        WIKI_REF_CHANGE: '修改链接',
    }


MOP = MANAGE_OPERATION  # alias


class ManageLog(BaseModel):
    id = BlobField(primary_key=True)  # 使用长ID
    user_id = BlobField(index=True, null=True)  # 操作用户
    role = TextField(null=True)  # 操作身份
    time = MyTimestampField(index=True)  # 操作时间
    related_type = IntegerField()  # 被操作对象类型
    related_id = BlobField(index=True)  # 被操作对象
    related_user_id = BlobField(index=True, null=True)  # 被操作对象涉及用户
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
    def add_by_post_changed(cls, view, key, operation, related_type, update_values, old_record, record, note=None,
                            *, value=NotImplemented, diff_func=save_couple):
        """
        如果指定的列发生了改变，那么新增一条记录，反之什么也不做
        :param view: 请求中的view对象，用于拿用户id和角色
        :param key: 指定的列名
        :param operation: 如果条件达成记录的操作
        :param related_type: 被改变的对象的类型
        :param update_values: 被提交上来的值，默认为字典，在其中检查key是否存在。若为bool则直接替代key存在与否的判定结果
        :param old_record: 应用改动前的值
        :param record: 应用改动后的值
        :param note: 备注信息
        :param value: 默认值为NotImplemented，实现为diff_func的返回结果，若修改则记为想要的值
        :param diff_func: 默认值为save_couple，实现为记录前后的变化[old_record[key], record[key]]
        :return:
        """

        def get_val(r, k):
            if isinstance(r, (DataRecord, dict)):
                return r[k]
            elif isinstance(r, BaseModel):
                return getattr(r, k)
            else:
                raise TypeError()

        def key_in_values():
            if isinstance(update_values, dict):
                return key in update_values
            elif isinstance(update_values, bool):
                return update_values
            else:
                raise TypeError()

        if key_in_values():
            old, new = get_val(old_record, key), get_val(record, key)
            if old == new: return  # 修改前后无变化
            if value is NotImplemented:
                value = diff_func(old, new)

            return cls.new(view.current_user.id, view.current_role, related_type, get_val(record, 'id'),
                           get_val(record, 'user_id'), operation, value, note=note)

    class Meta:
        db_table = 'manage_log'
