import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os
import api.chat
import api.main
import api.callback
import traceback


from tornado.web import RequestHandler
from tornado.options import define, options
from tornado.log import access_log, app_log, gen_log
from common.logger import logger, filehandler

define("port", default=8000, type=int)


class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")


def enable_tornado_log():
    """开启 Tornado 内置日志信息
    * ``tornado.access``: Per-request logging for Tornado's HTTP servers (and
      potentially other servers in the future)
    * ``tornado.application``: Logging of errors from application code (i.e.
      uncaught exceptions from callbacks)
    * ``tornado.general``: General-purpose logging, including any errors
      or warnings from Tornado itself.
    """
    try:
        access_log.addHandler(filehandler)
        access_log.setLevel(logger.level)

        app_log.addHandler(filehandler)
        app_log.setLevel(logger.level)

        gen_log.addHandler(filehandler)
        gen_log.setLevel(logger.level)
    except Exception:
        error_msg = traceback.format_exc()
        logger.warning(f'enable tornado log fail.\t{error_msg}')
        logger.error(f'enable tornado log fail.')


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/chat/(?P<user_id>\w+)", api.chat.ChatHandler),
        (r"/bot", api.main.BotRequest),
        (r"/callback", api.callback.CallbackHandler),
    ],
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        debug=True
    )
    port = options.port
    enable_tornado_log()
    logger.info(f'listening on {port}')
    logger.info(f"DEBUG is: True")
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
