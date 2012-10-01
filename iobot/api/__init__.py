import tornado.web
import tornado.auth

from iobot.api.handlers.auth import AuthHandler


class APIServer(object):
    """ manages a tornado instance for processing twitter oauth """

    def __init__(self, store, max_connections=5, tornado_port=8899):
        self._store = store
        self._max_connections = max_connections
        self._tornado_port = tornado_port
        self._start_tornado()

    # public:

    @property
    def auth_url(self):
        """ this shouldn't go here """
        return u''

    # private:

    def _start_tornado(self):
        self._application = self._get_app()
        self._application.listen(self._tornado_port, '0.0.0.0')

    def _get_app(self):
        # define the application
        routes = [
            (AuthHandler.URL, AuthHandler),
            ]

        # get that out of there...
        return tornado.web.Application(
            routes,
            store=self._store,
            debug=False
            )

    def _(self):
        pass

