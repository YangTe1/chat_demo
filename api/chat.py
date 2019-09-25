import datetime
from tornado.websocket import WebSocketHandler
from collections import defaultdict


class ChatHandler(WebSocketHandler):
    # users = set()  # 用来存放在线用户的容器
    users = defaultdict(set)  # 用来存放在线用户的容器

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.user_id = None

    def open(self, user_id):
        self.user_id = user_id
        self.users[user_id].add(self)  # 建立连接后添加用户到容器中
        # self.users.add(self)  # 建立连接后添加用户到容器中
        # for u in self.users:  # 向已在线用户发送消息
        #     u.write_message(
        #         u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        self.write_message(
            u"[%s]-[%s]-进入聊天室" % (user_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        for u in self.users:  # 向在线用户广播消息
            u.write_message(u"[%s]-[%s]-说：%s" % (
                self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    @classmethod
    async def ai_reply(cls, user_id, message):
        # for u in cls.users:  # 向在线用户广播消息
        #     u.write_message(u"[%s]-[%s]-说：%s" % (user_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
        for u in cls.users[user_id]:
            u.write_message(u"[%s]-[%s]-说：%s" % (
                user_id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        self.users[self.user_id].remove(self)  # 用户关闭连接后从容器中移除用户
        for u in self.users[self.user_id]:
            u.write_message(
                u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求
