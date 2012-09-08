import tornado.web
import tornado.auth


class AuthHandler(tornado.web.RequestHandler,
                  tornado.auth.TwitterMixin):

    URL = '/auth'

    """ Provides a temporary return socket for twitter auth """
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
        # return, and/or save the user now
        store = self.application.settings.store
        store.upsert({'nick': 'something'})
        #self.authorize_redirect()

