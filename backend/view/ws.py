from slim.base.ws import WSHandler
from view import route


@route('/ws')
class WSH(WSHandler):
    pass
