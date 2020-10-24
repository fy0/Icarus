from typing import Type

from crud.crud import c
from pycurd.crud.base_crud import BaseCrud
from slim.base.web import JSONResponse
from slim.view import CrudView


class BaseCrudView(CrudView):
    crud: BaseCrud = c
    is_base_class = True

    def finish(self, code, data=None, msg=None):
        self.response = JSONResponse(200, {
            'code': code,
            'data': data,
            'msg': msg
        })
