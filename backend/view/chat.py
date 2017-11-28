from slim.retcode import RETCODE
from view.ws import WSH


@WSH.route('chat.test')
async def chat_test(ws, send_json, data):
    await send_json(RETCODE.SUCCESS, None)
    await send_json(RETCODE.WS_DONE, None)
