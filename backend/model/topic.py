from model._post import POST_VISIBLE, POST_STATE, PostModel
from slim.utils import StateObject
from peewee import *
from model import db, BaseModel, MyTimestampField
from model.user import User
from model.board import Board

"""
顶贴机制：
1. 置顶权重，默认为0，如有置顶则设置其值，越高排在越上面
2. 一般权重，默认值为发帖时当前帖子个数，回帖、上升、下沉几个操作使其增加或减少，越高排在越上面
3. 时间，当以上两个权重相等的时候，越新的帖子排在越上面
"""


class Topic(PostModel):
    title = TextField(index=True)
    board_id = BlobField(index=True)

    edit_count = IntegerField(default=0)
    edit_time = MyTimestampField(index=True, null=True)
    last_edit_user_id = BlobField(index=True, null=True)
    content = TextField()

    awesome = IntegerField(default=0)  # 精华文章
    sticky_weight = IntegerField(index=True, default=0)  # 置顶权重
    weight = IntegerField(index=True, default=0) # 排序权值，越大越靠前，默认权重与id相同

    # object_type = OBJECT_TYPES.TOPIC

    class Meta:
        db_table = 'topic'

    @classmethod
    def weight_gen(cls):
        cur = db.execute_sql('select max(weight)+1 from "topic"')
        return cur.fetchone()[0] or 0

    def weight_inc(self):
        """ 提升一点排序权重 """
        try:
            db.execute_sql("""
                WITH
                  t1 as (SELECT "id", "weight" FROM "topic" WHERE "id" = %s),
                  t2 as (SELECT "t2"."id", "t2"."weight" FROM t1, "topic" AS t2
                    WHERE "t2"."weight" > "t1".weight ORDER BY "weight" ASC LIMIT 1)
                UPDATE "topic"
                  set "weight" = (
                    CASE WHEN "topic"."id" = "t1"."id"
                      THEN "t2"."weight"
                    ELSE "t1"."weight" END
                  )
                FROM t1, t2
                WHERE "topic"."id" in ("t1"."id", "t2"."id");
            """, (self.id,))
        except DatabaseError:
            pass
