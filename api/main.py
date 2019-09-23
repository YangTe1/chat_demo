import json

from tornado.web import RequestHandler
from wulaisdk.client import WulaiClient


class BotRequest(RequestHandler):
    async def post(self, *args, **kwargs):
        pubkey = "asEGUJtCyLkHvTmm8vE0bXLe5ebGs2PP00df19808441f2ceac"
        secret = "Ac6ogAAgaTXojvX2LFBS"
        client = WulaiClient(pubkey, secret)
        print(self.request.body)

        data = json.loads(self.request.body)
        print(data)
        msg = data["msg"]
        msg_body = {"text": {"content": msg}}
        user_id = data["user_id"]
        print(user_id)
        print(msg_body)

        client.create_user(user_id)
        resp = client.get_bot_response(user_id, msg_body)

        return self.write(resp.to_dict())
