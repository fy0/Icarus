from peewee import BlobField, BigIntegerField, TextField
from model import BaseModel, MyTimestampField
from model._post import LongIdPostModel


class UserUpload(LongIdPostModel):
    id = BlobField(primary_key=True)
    size = BigIntegerField()
    hash = BlobField(index=True)
    format = TextField()

    class Meta:
        db_table = 'user_upload'
