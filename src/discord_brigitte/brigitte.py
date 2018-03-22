import asyncio
import os
import sys
import logging

import discord

from discord.ext.commands import Bot
from discord.client import Client
from discord_brigitte.plugins.plugin_manager import PluginManager

from discord_brigitte.plugins.echo import Echo
from discord_brigitte.plugins.send_pic import SendPic
from discord_brigitte.plugins.pi_camera import PiCamera
from discord_brigitte.plugins.poc_playmusic import PocPlayMusic
from discord_brigitte.plugins.stop_brigitte import StopBrigitte

TOKEN = os.getenv('BRIGITTEORDEL_TOKEN')
BRIGITTE_CHANNEL = os.getenv("BRIGITTEORDEL_CHANNEL")
BRIGITTE_VOICE_CHANNEL = os.getenv("BRIGITTEORDEL_VOICE_CHANNEL")
COMMAND_PREFIX = "b!"
DESCRIPTION = "A personal assistant disguised as a Discord bot"
VERSION = "0.0.1"

LOGGER = logging.getLogger("discord_brigitte.%s" % __name__)


class Brigitte(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()
        self.voice_channel_id = BRIGITTE_VOICE_CHANNEL


    async def on_ready(self):
        LOGGER.info('Logged in as')
        LOGGER.info(self.user.name)
        LOGGER.info(self.user.id)
        LOGGER.info('------')
        LOGGER.info("I will be your shield! Ready for combat!")


def configure_logging(is_debug=False):
    log_format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    logging.basicConfig(format=log_format,
                        filename='discord_brigitte.log',
                        level=logging.DEBUG if is_debug else logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(logging.DEBUG)
    # Add it to the root logger
    logging.getLogger('').addHandler(console_handler)

    LOGGER.info("******* Brigitte Ordel - I'll be your Discord bot! *******")
    LOGGER.debug("Ready to DEBUG!")


def main():
    configure_logging()
    bot = Brigitte(command_prefix=COMMAND_PREFIX, description=DESCRIPTION, pm_help=True)
    LOGGER.info("Running Brigitte!")
    bot.run(TOKEN)


if __name__ == '__main__':
    main()