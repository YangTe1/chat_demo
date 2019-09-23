import json

from tornado.web import RequestHandler
from common.logger import logger
from api.chat import ChatHandler


class CallbackHandler(RequestHandler):
    """
    接收吾来平台回调, 返回信息给客户端
    """

    async def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        content = data["msg_body"]["text"]["content"]
        user_id = data["user_id"]
        logger.warning(f"{content}")
        logger.warning(f"{user_id}")
        # do sth.
        # websocket服务
        # await UserSocketHandler.ai_reply(content, user_id)
        await ChatHandler.ai_reply(user_id, content)
        self.write("success")
