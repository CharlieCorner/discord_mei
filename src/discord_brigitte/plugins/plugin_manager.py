import logging

from discord_brigitte.plugins.plugin import Plugin

LOGGER = logging.getLogger("discord_brigitte.%s" % __name__)


class PluginManager:

    def __init__(self, brigitte):
        self.brigitte = brigitte
        self.brigitte.plugins = []

    def load(self, plugin):
        LOGGER.info('Loading plugin {}.'.format(plugin.__name__))
        plugin_instance = plugin(self.brigitte)
        self.brigitte.plugins.append(plugin_instance)

        for comm in plugin_instance.get_commands():
            self.brigitte.add_command(comm)

        LOGGER.info('Plugin {} loaded.'.format(plugin.__name__))

    def load_all(self):
        for plugin in Plugin.plugins:
            self.load(plugin)
