import time
from typing import Mapping, Dict

import config
from slim.support.peewee import PeeweeView
from model.board import Board
from slim.utils import ObjectID
from view import route


@route('board')
class UserView(PeeweeView):
    model = Board

    @staticmethod
    def handle_read(values: Dict):
        pass

    @staticmethod
    def handle_insert(values: Dict):
        values['id'] = config.ID_GENERATOR().digest()
        values['time'] = int(time.time())
