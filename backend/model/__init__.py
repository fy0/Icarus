import time

from . import redis
from slim.utils import async_run
import config

# asyncpg 配置

import asyncpg

# TODO: 连接池
asyncpg_conn = None


def asyncpg_init(db_uri):
    async def create_conn():
        global asyncpg_conn
        # : asyncpg.connection.Connection
        asyncpg_conn = await asyncpg.connect(db_uri)

    async_run(create_conn)


# asyncpg_init(config.DATABASE_URI)

# peewee 配置

import peewee
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict


db = connect(config.DATABASE_URI)


class CITextField(peewee.TextField):
    field_type = 'CITEXT'


class SerialField(peewee.IntegerField):
    field_type = 'SERIAL'


class INETField(peewee.TextField):
    # 临时解决方案，peewee 的 custom field 有点问题
    field_type = 'inet'


class MyTimestampField(peewee.BigIntegerField):
    pass


class BaseModel(peewee.Model):
    class Meta:
        database = db

    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_by_pk(cls, value):
        try:
            return cls.get(cls._meta.primary_key == value)
        except cls.DoesNotExist:
            return

    @classmethod
    def exists_by_pk(cls, value):
        return cls.select().where(cls._meta.primary_key == value).exists()


def get_time():
    return int(time.time())


class StdModel(BaseModel):
    id = peewee.BlobField(primary_key=True)
    time = peewee.BigIntegerField(index=True, default=get_time)
    deleted_at = peewee.BigIntegerField(null=True, index=True)

    is_for_tests = peewee.BooleanField(default=False, help_text='单元测试专属账号，单元测试结束后删除')


class StdUserModel(StdModel):
    user_id = peewee.BlobField(index=True, null=True, help_text='创建者用户ID')
