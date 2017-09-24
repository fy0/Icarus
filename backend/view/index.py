from model.board import BOARD_STATE
from slim.base.view import BasicView
from slim.retcode import RETCODE
from view import route


@route('/misc')
class TestViewBasic(BasicView):
    @classmethod
    def interface(cls):
        cls.use('info', 'GET')

    async def info(self):
        self.finish(RETCODE.SUCCESS, {
            'BOARD_STATE': BOARD_STATE.to_dict(),
            'BOARD_STATE_TXT': BOARD_STATE.txt,
            'retcode': list(RETCODE.items()),
            'retinfo_cn': RETCODE.txt_cn,
        })
