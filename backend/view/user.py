from slim.support.peewee import PeeweeView
from model.user import User


class UserView(PeeweeView):
    model = User
