from model.user import User
from slim.base.ws import WSRouter
from slim.utils import to_bin

'''
@route.websocket('/ws')
class WSR(WSRouter):
    def teardown_user_key(self):
        u: User = self.current_user
        u.key = None
        u.save()

    def get_user_by_key(self, key):
        if not key: return
        try: return User.get_by_key(to_bin(key))
        except: pass
'''
