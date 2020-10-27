import time
import config
from typing import Dict, List

from api.view.curd import BaseCrudUserView
from app import app
from crud.schemas.topic import Topic
from model.topic_model import TopicModel
from api import cooldown, same_user, run_in_thread

#
# def my_optional(form, field):
#     if field.data is None:
#         raise StopValidation()
#
#
# def board_check(form, field):
#     """
#     检查板块是否存在，是否可以允许当前用户创建文章或写入
#     """
#     try:
#         board_id = to_bin(field.data)
#     except TypeError:
#         raise ValidationError('板块ID无效')
#     board = BoardModel.get_by_id(board_id)
#     if not board:
#         raise ValidationError('板块不存在')
#
#     can_post_rank = 100 if set(form.view.roles) & {'forum_master', 'superuser', 'admin'} else 0
#     if can_post_rank >= board.can_post_rank:
#         return True
#     raise ValidationError('没有权限选择此板块')
#
#
# class TopicNewForm(ValidateForm):
#     title = StringField('标题', validators=[
#         va.required(),
#         va.Length(config.TOPIC_TITLE_LENGTH_MIN, config.TOPIC_TITLE_LENGTH_MAX)
#     ])
#
#     content = StringField('正文', validators=[
#         va.required(),
#         va.Length(1, config.TOPIC_CONTENT_LENGTH_MAX)
#     ])
#
#     sticky_weight = IntegerField('置顶权重', validators=[])
#     weight = IntegerField('排序权重', validators=[])
#     board_id = StringField('板块', validators=[va.required(), board_check])
#
#
# class TopicEditForm(ValidateForm):
#     title = StringField('标题', validators=[
#         va.optional(),
#         va.Length(config.TOPIC_TITLE_LENGTH_MIN, config.TOPIC_TITLE_LENGTH_MAX)
#     ])
#
#     content = StringField('正文', validators=[
#         va.optional(),
#         va.Length(1, config.TOPIC_CONTENT_LENGTH_MAX)
#     ])
#
#     sticky_weight = IntegerField('置顶权重', validators=[])
#     weight = IntegerField('排序权重', validators=[])
#     board_id = StringField('板块', validators=[
#         my_optional,
#         board_check
#     ])


@app.route.view('topic')
class TopicView(BaseCrudUserView):
    model = Topic

    @classmethod
    def ready(cls):
        cls.add_soft_foreign_key('id', 'post_stats')
        cls.add_soft_foreign_key('user_id', 'user')
        cls.add_soft_foreign_key('board_id', 'board')
        cls.add_soft_foreign_key('last_edit_user_id', 'user')

    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_IP, b'ic_cd_topic_new_%b', cd_if_unsuccessed=10)
    @cooldown(config.TOPIC_NEW_COOLDOWN_BY_ACCOUNT, b'ic_cd_topic_new_account_%b', unique_id_func=same_user, cd_if_unsuccessed=10)
    async def insert(self):
        return await super().insert()


'''
from slim.utils.debug import Debug

debug = Debug()
debug.add_view(TopicView, TopicForm)
debug.serve(route, '/debug')
'''
