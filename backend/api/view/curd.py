from typing import Type

from api.user_view_mixin import UserViewMixin
from crud.crud import c
from pycurd.crud.base_crud import BaseCrud
from slim.base.web import JSONResponse
from slim.retcode import RETCODE
from slim.view import CrudView


class BaseCrudView(CrudView):
    crud: BaseCrud = c
    is_base_class = True

    def on_finish(self):
        if self._route_info.handler == self.__class__.get:
            if self.response.data is None:
                self.finish(RETCODE.NOT_FOUND)

        if self.response.data and isinstance(self.response.data, dict) and 'code' in self.response.data:
            self.response = JSONResponse(200, {
                'code': RETCODE.SUCCESS,
                'data': self.response.data,
                'msg': ''
            })

        # print(1111, self._route_info.handler, self.__class__.get)
        # print(self.response)

    def finish(self, code, data=None, msg=None):
        self.response = JSONResponse(200, {
            'code': code,
            'data': data,
            'msg': msg
        })


class BaseCrudUserView(UserViewMixin, BaseCrudView):
    is_base_class = True
