import tornado.ioloop
import tornado.web
import tornado.auth

from iobot.handlers.auth import AuthHandler


class APIServer(object):
    """ manages a tornado instance for processing twitter oauth """

    def __init__(self, max_connections=5, tornado_port=8899):
        self._max_connections = max_connections
        self._tornado_port = tornado_port
        self._ioloop = None

        self._start_tornado()

    # public:

    @property
    def auth_url(self):
        """ this shouldn't go here """
        return u''

    # private:

    def _start_tornado(self):
        self._ioloop = self._ioloop or tornado.ioloop.IOLoop.instance()
        if not self._ioloop.running():
            self._application = self.get_app()
            self._application.listen(self.available_port(), '0.0.0.0')
            self._ioloop.start()


    def _get_app(self):
        # define the application
        return = tornado.web.Application([
            (AuthHandler.URL, AuthHandler),
            ])

    def _(self):
        pass

