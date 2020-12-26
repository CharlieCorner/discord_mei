import logging
import os
import sys

import aiohttp
from discord.ext.commands import Bot

from plugins.plugin_manager import PluginManager

TOKEN = os.environ.get('MEIORDEL_TOKEN')
MEI_CHANNEL = os.environ.get("MEIORDEL_CHANNEL")
MEI_VOICE_CHANNEL = os.environ.get("MEIORDEL_VOICE_CHANNEL")

COMMAND_PREFIX = "m!"
DESCRIPTION = "A personal assistant disguised as a Discord bot"
VERSION = "0.0.1"

LOGGER = logging.getLogger("discord_mei.%s" % __name__)


class Mei(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()
        self.voice_channel_id = MEI_VOICE_CHANNEL

    async def on_ready(self):
        LOGGER.info('Logged in as')
        LOGGER.info(self.user.name)
        LOGGER.info(self.user.id)
        LOGGER.info('------')
        LOGGER.info("I will be your shield! Ready for combat!")


def configure_logging(is_debug=False):
    log_format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    logging.basicConfig(format=log_format,
                        filename='discord_mei.log',
                        level=logging.DEBUG if is_debug else logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(logging.DEBUG)
    # Add it to the root logger
    logging.getLogger('').addHandler(console_handler)

    LOGGER.info("******* Mei Ordel - I'll be your Discord bot! *******")
    LOGGER.debug("Ready to DEBUG!")


def main():
    configure_logging()
    bot = Mei(command_prefix=COMMAND_PREFIX,
              description=DESCRIPTION,
              pm_help=True,
              connector=aiohttp.TCPConnector(verify_ssl=False))
    LOGGER.info("Running Mei!")
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
