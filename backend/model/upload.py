from peewee import BlobField, BigIntegerField, TextField
from model import BaseModel, MyTimestampField
from model._post import LongIdPostModel


class UploadEntity(BaseModel):
    """
    id 为文件哈希，这个表对应实际的文件
    """
    id = BlobField(primary_key=True)
    time = MyTimestampField(index=True)  # 发布时间
    size = BigIntegerField()
    format = TextField(index=True)

    class Meta:
        db_table = 'upload_entity'


class Upload(LongIdPostModel):
    hash = BlobField()

    class Meta:
        db_table = 'uploads'
