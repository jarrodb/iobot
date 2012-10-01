
from iobot.plugins import TextPlugin
from iobot.plugins.decorators import plugin_command

class CorePlugin(TextPlugin):

    NAME = 'core'

    @plugin_command
    def reregister(self, irc):
        """ re-register's the plugin <irc.command>"""
        irc._bot.reload_plugin(irc.command_args)


