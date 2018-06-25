import time
from peewee import BlobField, BigIntegerField, TextField
from playhouse.postgres_ext import BinaryJSONField

import config
from model import BaseModel, MyTimestampField
from model._post import LongIdPostModel


class Upload(LongIdPostModel):
    id = BlobField(primary_key=True)
    key = TextField(index=True)
    size = BigIntegerField()
    ext = TextField(null=True)
    type_name = TextField(null=True, default=None)
    image_info = BinaryJSONField(null=True, default=None)

    class Meta:
        db_table = 'upload'

    @classmethod
    def new(cls, user_id, key, size, ext=None, type_name=None, image_info=None):
        # 之所以有key的情况下还有独立id，是因为上传是一个一对多的过程，多个用户可能上传同一张图片，那么key就相同
        return cls.create(id=config.LONG_ID_GENERATOR().digest(), time=int(time.time()), user_id=user_id,
                          key=key, size=int(size), ext=ext, type_name=type_name, image_info=image_info)
