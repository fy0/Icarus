import config
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

            'USERNAME_MIN': config.USERNAME_MIN,
            'USERNAME_MAX': config.USERNAME_MAX,
            'USERNAME_FOR_REG_MIN': config.USERNAME_FOR_REG_MIN,
            'USERNAME_FOR_REG_MAX': config.USERNAME_FOR_REG_MAX,
            'PASSWORD_MIN': config.PASSWORD_MIN,
            'PASSWORD_MAX': config.PASSWORD_MAX,

            'retcode': RETCODE.to_dict(),
            'retinfo_cn': RETCODE.txt_cn,
        })
