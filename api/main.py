import json

from tornado.web import RequestHandler
from wulaisdk.client import WulaiClient
# from api.chat import ChatHandler


class BotRequest(RequestHandler):
    async def post(self, *args, **kwargs):
        pubkey = "asEGUJtCyLkHvTmm8vE0bXLe5ebGs2PP00df19808441f2ceac"
        secret = "Ac6ogAAgaTXojvX2LFBS"
        client = WulaiClient(pubkey, secret)

        data = json.loads(self.request.body)
        msg = data["msg"]
        msg_body = {"text": {"content": msg}}
        user_id = data["user_id"]

        client.create_user(user_id)
        resp = client.receive_message(user_id, msg_body)

        return self.write(resp.to_dict())
        # await ChatHandler.ai_reply(user_id, "hhhhhhh")
        # self.write("success")
