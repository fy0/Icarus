from slim.utils import async_run
import config

# asyncpg 配置

import asyncpg

# TODO: 连接池
asyncpg_conn = None


def asyncpg_init(db_uri):
    async def create_conn():
        global asyncpg_conn
        asyncpg_conn: asyncpg.connection.Connection = await asyncpg.connect(db_uri)

    async_run(create_conn)


asyncpg_init(config.DATABASE_URI)

# peewee 配置

import peewee
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
# from model.redis import redis


db = connect(config.DATABASE_URI)


class CITextField(peewee._StringField):
    db_field = 'citext'


class SerialField(peewee.IntegerField):
    db_field = 'serial'


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
