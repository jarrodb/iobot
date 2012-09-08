import tornado.web
import tornado.auth

from iobot.handlers.auth import AuthHandler


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

        return tornado.web.Application(
            routes,
            twitter_consumer_key='FcwhVFaLVlkupO97GF12Rw',
            twitter_consumer_secret='JEGIeELh0GGdYr0nGfmy1S4E9iBdBI1OiT0O6OoSXw',
            store=self._store,
            debug=True
            )

    def _(self):
        pass

