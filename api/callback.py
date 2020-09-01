import json
import websocket

from tornado.web import RequestHandler
from common.logger import logger
from api.chat import ChatHandler


# class CallbackHandler(RequestHandler):
#     """
#     接收吾来平台回调, 返回信息给客户端
#     """
#
#     async def post(self, *args, **kwargs):
#         data = json.loads(self.request.body)
#         content = data["msg_body"]["text"]["content"]
#         user_id = data["user_id"]
#         logger.warning(f"{content}")
#         logger.warning(f"{user_id}")
#         # do sth.
#         # websocket服务
#         await ChatHandler.ai_reply(user_id, content)
#
#         self.write("success")


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
        msg = {"user_id": user_id, "data": content}
        # do sth.
        # websocket服务
        ws = websocket.WebSocket()
        ws.connect(f"ws://39.96.21.121:8646/chat/{user_id}")
        ws.send(f"{msg}")
        ws.close()
        # ws.recv()
        # await ChatHandler.ai_reply(user_id, content)

        self.write("success")
