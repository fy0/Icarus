from peewee import *
from playhouse.postgres_ext import ArrayField
from model import BaseModel
from model.user import User


class Statistic(BaseModel):
    id = BlobField(primary_key=True)
    views = ArrayField(BlobField)
    click_count = IntegerField(default=0)
    follow_count = IntegerField(default=0)
    comment_count = IntegerField(default=0)

    class Meta:
        db_table = 'statistic'
