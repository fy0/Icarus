from slim.retcode import RETCODE
from slim.tools.request import do_request, SlimViewRequest

__all__ = ['user', 'board', 'topic', 'comment', 'misc']

token = None

config = {
    'remote': {
        'API_SERVER': 'http://localhost:9999',
        'WS_SERVER': 'ws://localhost:9999/ws',
        'authMode': 'access_token' # access_token / access_token_in_params / cookie
    },
    'access_token': None
}


class UserViewRequest(SlimViewRequest):
    def signin(self, email, password):
        resp = do_request(self.config, 'POST', f'{self.urlPrefix}/signin', {}, {'email': email, 'password': password}, None)
        if resp:
            ret = resp.json()
            if ret['code'] == RETCODE.SUCCESS:
                self.config['access_token'] = ret['data']['access_token']
            return ret

    def get_userid(self):
        return do_request(self.config, 'GET', f'{self.urlPrefix}/get_userid', null).json()

    def signout(self):
        return do_request(self.config, 'POST', f'{self.urlPrefix}/signout', {}).json()


def misc():
    return do_request(config, 'GET', f"{config['remote']['API_SERVER']}/api/misc/info", {}).json()


user = UserViewRequest(config, 'user')
board = SlimViewRequest(config, 'board')
topic = SlimViewRequest(config, 'topic')
comment = SlimViewRequest(config, 'comment')
