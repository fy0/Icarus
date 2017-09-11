
import asyncio
import asyncpg
from lib.pvpatch import apply_to_dict_patch
apply_to_dict_patch()

import math
import config
import peewee
import playhouse.gfk
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
from model.redis import redis

asyncpg_conn = None
db = connect(config.PGDATABASE_URI)


def asyncpg_init(db_uri):
    async def create_conn():
        global asyncpg_conn
        asyncpg_conn = await asyncpg.connect(db_uri)

    asyncio.get_event_loop().run_until_complete(create_conn())

asyncpg_init(config.PGDATABASE_URI)


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

