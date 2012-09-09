import tweepy

from iobot.plugins import TextPlugin
from iobot.plugins.decorators import plugin_command

class CoreAuth(TextPlugin):

    key = "FcwhVFaLVlkupO97GF12Rw"
    secret = "JEGIeELh0GGdYr0nGfmy1S4E9iBdBI1OiT0O6OoSXw"

    @plugin_command
    def whoami(self, irc):
        if irc.user and irc.user.auth:
            irc.say("authenticated: %s" % irc.user.nick)
        else:
            irc.say("unauthenticated")

    @plugin_command
    def auth(self, irc):
        if irc.chan != irc._bot.nick: raise UserWarning('Do not auth publicly')
        auth_url = self._auth_url(irc)
        irc.say("auth url: %s" % auth_url, irc.nick)

    @plugin_command
    def authpin(self, irc):
        if irc.chan != irc._bot.nick: raise UserWarning('Public pin?  lol')
        verifier = irc.command_args

        try:
            auth = tweepy.OAuthHandler(self.key, self.secret)
            auth.set_request_token(
                irc.user['token_key'],
                irc.user['token_secret'] )
            auth.get_access_token(verifier)

        except Exception, e:
            print e
            irc.say('Authentication error', irc.nick)

        else:
            irc.user['auth'] = True
            irc._bot.store.upsert(irc.user)
            irc.say('Authentication successful', irc.nick)

    def _auth_url(self, irc):
        #http://errorsandexceptions.wordpress.com/2010/12/08/using-oauth-with-python-twitter-tools/
        try:
            auth = tweepy.OAuthHandler(self.key, self.secret)

            redirect_url = auth.get_authorization_url()

            irc._bot.store.upsert({
                'nick': irc.nick,
                'mask': irc.mask,
                'token_key': auth.request_token.key,
                'token_secret': auth.request_token.secret,
                'auth': False,
                })

        except Exception, e:
            print e

        return redirect_url
