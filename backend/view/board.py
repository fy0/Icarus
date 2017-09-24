from typing import Mapping, Dict

import time

from slim.support.peewee import PeeweeView
from model.board import Board
from slim.utils import ObjectID
from view import route


@route('board')
class UserView(PeeweeView):
    model = Board

    def handle_read(self, values: Dict):
        return values

    def handle_insert(self, values: Dict):
        values['id'] = ObjectID().digest()
        values['time'] = int(time.time())
        return values
