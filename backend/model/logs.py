from peewee import *
from playhouse.postgres_ext import BinaryJSONField
from model import BaseModel, MyTimestampField
from model.user import User
from slim import json_ex_dumps
from slim.utils import StateObject


class MANAGE_OPERATION(StateObject):
    POST_STATE_CHANGE = 0  # 改变状态：例如删除等等
    POST_VISIBLE_CHANGE = 1

    TOPIC_BOARD_MOVE = 20  # 移动主题到其他板块
    TOPIC_BOARD_EDIT = 21  # 修改主题
    TOPIC_BOARD_AWESOME_CHANGE = 22  # 移动主题到其他板块
    TOPIC_BOARD_STICKY_WEIGHT_CHANGE = 24
    TOPIC_BOARD_WEIGHT_CHANGE = 25

    USER_PASSWORD_CHANGE = 40  # 设置用户密码（未来再做区分，现在进有这个）
    USER_PASSWORD_RESET = 41  # 重置用户密码
    USER_KEY_RESET = 42
    USER_GROUP_CHANGE = 43
    USER_CREDIT_CHANGE = 44
    USER_REPUTATION_CHANGE = 45

    txt = {
        POST_STATE_CHANGE: '改变状态',
        POST_VISIBLE_CHANGE: '修改可见度',

        TOPIC_BOARD_MOVE: '移动主题',
        TOPIC_BOARD_EDIT: '修改主题',
        TOPIC_BOARD_AWESOME_CHANGE: '设置优秀文章',
        TOPIC_BOARD_STICKY_WEIGHT_CHANGE: '修改置顶权重',
        TOPIC_BOARD_WEIGHT_CHANGE: '修改板块权重',

        USER_PASSWORD_CHANGE: '重置用户密码',
        USER_KEY_RESET: "重置用户访问令牌",
        USER_GROUP_CHANGE: '修改用户组',
        USER_CREDIT_CHANGE: '积分变更',
        USER_REPUTATION_CHANGE: "声望变更",
    }


class ManageLog(BaseModel):
    id = BlobField(primary_key=True)  # 使用长ID
    user_id = BlobField(index=True)  # 操作用户
    time = MyTimestampField(index=True)  # 操作时间
    related_id = BlobField(index=True)  # 被操作对象
    related_type = IntegerField()  # 被操作对象类型
    operation = IntegerField()  # 操作行为
    value = BinaryJSONField(dumps=json_ex_dumps)  # 操作数据

    class Meta:
        db_table = 'manage_log'
