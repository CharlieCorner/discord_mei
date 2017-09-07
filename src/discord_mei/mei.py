import asyncio
import os
import sys
import logging

import discord

from discord.ext.commands import Bot
from discord.client import Client
from discord_mei.plugins.plugin_manager import PluginManager

from discord_mei.plugins.echo import Echo
from discord_mei.plugins.send_pic import SendPic
from discord_mei.plugins.pi_camera import PiCamera
from discord_mei.plugins.poc_playmusic import PocPlayMusic
from discord_mei.plugins.stop_mei import StopMei

TOKEN = os.getenv('MEIORDEL_TOKEN')
MEI_CHANNEL = os.getenv("MEIORDEL_CHANNEL")
MEI_VOICE_CHANNEL = os.getenv("MEIORDEL_VOICE_CHANNEL")
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
        LOGGER.info('Mei ready for combat! :)')


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

    LOGGER.info("******* Mei Ordel - Discord is worth fighting for! *******")
    LOGGER.debug("Ready to DEBUG!")


def main():
    configure_logging()
    bot = Mei(command_prefix=COMMAND_PREFIX, description=DESCRIPTION, pm_help=True)
    LOGGER.info("Running Mei!")
    bot.run(TOKEN)


if __name__ == '__main__':
    main()