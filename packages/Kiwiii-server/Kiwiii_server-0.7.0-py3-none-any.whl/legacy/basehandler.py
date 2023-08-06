import time
import uuid

from tornado import web, websocket, gen
from cheddar.data.webdataframe import Dataframe

USER = "guest"
PASSWORD = "pass"

# TODO: move to dbhandler(how?)
HIDDEN_PROPS = ("_mol", "_mw_wo_sw", "_logp", "_formula", "_aliases")


class DataframeContainer(object):
    """Manage dataframes used in web application."""
    def __init__(self):
        self.container = {}
        self.df_max_age = 86400 * 7  # Time(sec)

    def register(self):
        """Register new dataframe with unique ID."""
        id_ = str(uuid.uuid4())
        # at least 2 cols are required for datatable.js initialization
        self.update(id_, None, ("", ""))
        return id_

    def unregister(self, id_):
        del self.container[id_]

    def set_expires(self, id_):
        self.container[id_].expires = time.time() + self.df_max_age

    def update(self, id_, data, cols=None):
        if cols is None:
            cols = self.container[id_].columns()
        df = Dataframe(data=data, names=cols)
        for hp in HIDDEN_PROPS:
            if hp in cols:
                df[hp].visible = False
        self.container[id_] = df
        self.set_expires(id_)

    def remove_expired(self):
        now = time.time()
        dels = []
        for k, v in self.container.items():
            if v.expires < now:
                dels.append(k)
        for d in dels:
            self.unregister(d)


class BaseHandler(web.RequestHandler):
    def initialize(self, dfcont, wqueue):
        self.dfcont = dfcont
        self.wqueue = wqueue

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_df(self):
        id_ = self.get_cookie("df")  # None if no cookie
        try:
            df = self.dfcont.container[id_]
        except KeyError:
            id_ = self.dfcont.register()
            self.set_cookie("df", id_)
            return self.dfcont.container[id_]
        self.dfcont.set_expires(id_)
        return df


class StatusHandler(websocket.WebSocketHandler):
    def initialize(self, dfcont, wqueue):
        self.dfcont = dfcont
        self.wqueue = wqueue

    def on_message(self, message):
        df_id, abort = message.split(",")
        if int(abort):
            self.wqueue.abort(df_id)
            print("interruption requested")
            return
        else:
            self.watch(df_id)

    @gen.coroutine
    def watch(self, df_id):
        while 1:
            s = self.wqueue.status(df_id)
            try:
                self.write_message(s)
            except websocket.WebSocketClosedError:
                break
            if s == "Completed":
                break
            yield gen.sleep(1)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html", warn_incorrect=False)

    def post(self):
        user = self.get_argument("name")
        pw = self.get_argument("pass")
        if user == USER and pw == PASSWORD:
            id_ = self.dfcont.register()
            self.set_secure_cookie("user", user)
            self.set_cookie("df", id_)
            self.redirect("/")
        else:
            self.render("login.html", warn_incorrect=True)


class LogoutHandler(BaseHandler):
    def get(self):
        self.dfcont.unregister(self.get_cookie("df"))
        self.clear_cookie("user")
        self.clear_cookie("df")
        self.redirect("/")


class ShowColumnsHandler(BaseHandler):
    @web.authenticated
    def post(self):
        cols = self.get_arguments("cols")
        df = self.get_df()
        for c in df.columns():
            if c in cols:
                df[c].visible = True
            else:
                df[c].visible = False
        self.redirect('/')


class UpdateHandler(BaseHandler):
    @web.authenticated
    def get(self):
        df = self.get_df()
        json_dict = {"data": list(df.rows_iter())}
        self.write(json_dict)
