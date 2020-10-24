from playhouse.postgres_ext import BinaryJSONField
from slim.base.user import BaseUser

from peewee import *

from model._post import LongIdPostModel
from model import BaseModel, MyTimestampField, CITextField, db, SerialField, user_model


class UserOAuth(LongIdPostModel):
    # 表字段
    login_id = IntegerField(null=False)  # 平台用户的id
    platform = TextField(null=True)  # 平台  各平台用户id可能会一样，只能作为对应平台的唯一标识。

    github_access_token = TextField(null=True)  # token
    github_user_info = BinaryJSONField(null=True)  # 用户数据
    qq_access_token = TextField(null=True)
    qq_user_info = BinaryJSONField(null=True)
    weibo_access_token = TextField(null=True)
    weibo_user_info = BinaryJSONField(null=True)


    # add other platform columns
    # qq_access_token
    # qq_user_info

    class Meta:
        db_table = 'user_oauth'

