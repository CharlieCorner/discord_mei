import logging

from discord_mei.plugins.plugin import Plugin

LOGGER = logging.getLogger("discord_mei.%s" % __name__)


class PluginManager:

    def __init__(self, mei):
        self.mei = mei
        self.mei.plugins = []

    def load(self, plugin):
        LOGGER.info('Loading plugin {}.'.format(plugin.__name__))
        plugin_instance = plugin(self.mei)
        self.mei.plugins.append(plugin_instance)

        for comm in plugin_instance.get_commands():
            self.mei.add_command(comm)

        LOGGER.info('Plugin {} loaded.'.format(plugin.__name__))

    def load_all(self):
        for plugin in Plugin.plugins:
            self.load(plugin)
