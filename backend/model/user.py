from peewee import *
from slim.utils import StateObject
from model import BaseModel


class USER_GROUP(StateObject):
    BAN = 10
    INACTIVE = 40
    NORMAL = 50
    ADMIN = 100

    txt = {BAN: '封禁', INACTIVE: '未激活', NORMAL: '会员', ADMIN: '管理'}


class USER_STATE(StateObject):
    DEL = 0
    NORMAL = 50

    txt = {DEL: '删除', NORMAL: '正常'}


class User(BaseModel):
    id = BlobField(primary_key=True)
    username = CharField(index=True, unique=True, max_length=32)
    nickname = CharField(index=True, max_length=32, null=True, default=None)
    password = BlobField()
    salt = BlobField()

    group = IntegerField(index=True)
    state = IntegerField(index=True)

    key = BlobField(index=True)
    key_time = BigIntegerField()
    reg_time = BigIntegerField()

    class Meta:
        db_table = 'user'

    #object_type = OBJECT_TYPES.USER
