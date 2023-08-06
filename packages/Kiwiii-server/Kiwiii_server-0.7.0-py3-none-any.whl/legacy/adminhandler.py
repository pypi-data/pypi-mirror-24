
import time

from chemex.util import debug
from tornado import web

from cheddar.basehandler import BaseHandler


class SessionsHandler(BaseHandler):
    @web.authenticated
    def get(self):
        contents = []
        for id_, df in self.dfcont.container.items():
            expires = time.strftime("%b %d %Y %H:%M:%S",
                                    time.localtime(df.expires))
            contents.append((id_, debug.total_size(df), expires))
        self.render("sessions.html", items=contents)


class TestHandler(BaseHandler):
    @web.authenticated
    def get(self):
        self.render("test.html")
