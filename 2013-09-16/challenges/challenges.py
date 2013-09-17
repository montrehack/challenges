__author__ = 'Gabriel Tremblay - initnull@gmail.com'

import config
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os

from level1 import Level1Handler
from level2 import Level2Handler
from level3 import Level3Handler
from level4 import Level4Handler

# Set-up
basedir = os.path.dirname(__file__)
application = tornado.web.Application(
    [
        (r"/", tornado.web.RedirectHandler, {"url": config.level1_link + ""}),
        (config.level1_link + ".*", Level1Handler),
        (config.level2_link + ".*", Level2Handler),
        (config.level3_link + ".*", Level3Handler),
        (config.level4_link + ".*", Level4Handler),
    ],
    # Options
    debug=False,
    xsrf_cookies=True,
    static_path=os.path.join(basedir, 'static'),
)

# Main
if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(
        application,
        # Why would you cheat anyway? :)
        ssl_options={
        "certfile": os.path.join(basedir, "server.crt"),
        "keyfile": os.path.join(basedir, "server.key"),
        }
    )

    # Boot!
    server.listen(config.listen_port)
    tornado.ioloop.IOLoop.instance().start()