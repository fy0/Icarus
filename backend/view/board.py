from slim.support.peewee import PeeweeView
from model.board import Board
from view import route


@route('board')
class UserView(PeeweeView):
    model = Board
