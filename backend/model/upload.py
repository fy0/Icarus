import time

import peewee
from peewee import BlobField, BigIntegerField, TextField
from playhouse.postgres_ext import BinaryJSONField
from slim.utils import StateObject, to_hex

import config
from model import BaseModel, MyTimestampField
from model._post import LongIdPostModel, POST_TYPES


class UPLOAD_SOURCE(StateObject):
    DEFAULT = None  # 默认，直接上传
    QINIU = 'qiniu'  # 七牛

    txt = {DEFAULT: "默认", QINIU: '七牛'}


class Upload(LongIdPostModel):
    key = TextField(index=True, help_text='哈希值')  # 为text的目的是兼容七牛等cdn站点，否则应该为blob
    size = BigIntegerField(help_text='图片文件大小')
    ext = TextField(null=True)
    type_name = TextField(null=True, default=None)
    image_info = BinaryJSONField(null=True, default=None)
    filename = TextField(null=True, index=True)
    source = TextField(null=True, index=True)

    class Meta:
        db_table = 'upload'

    @classmethod
    def get_by_key(cls, key: str):
        try:
            return cls.get(cls.key == key)
        except peewee.DoesNotExist:
            pass

    @classmethod
    def new_with_user(cls, user_id: bytes, hashes: bytes, filename: str, filesize: int):
        key = to_hex(hashes)
        values = {
            'user_id': user_id,
            'key': key,
            'filename': filename,
            'size': filesize
        }
        return cls.new(**values)

    @classmethod
    def new(cls, user_id, key, size, ext=None, type_name=None, image_info=None, filename=None, source=None):
        # 之所以有key的情况下还有独立id，是因为上传是一个一对多的过程，多个用户可能上传同一张图片，那么key就相同
        return cls.create(user_id=user_id, key=key, size=int(size), ext=ext, type_name=type_name,
                          image_info=image_info, source=source, filename=filename)

    @classmethod
    def get_post_type(cls):
        return POST_TYPES.UPLOAD
