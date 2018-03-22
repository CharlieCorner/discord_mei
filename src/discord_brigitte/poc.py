import os
import discord
from discord.ext import commands
from discord import Client

TOKEN = os.getenv('BRIGITTEORDEL_TOKEN')
BRIGITTE_CHANNEL = os.getenv("BRIGITTEORDEL_CHANNEL")
BRIGITTE_VOICE_CHANNEL = os.getenv("BRIGITTEORDEL_VOICE_CHANNEL")

description = '''A personal assistant disguised as a Discord bot'''
bot = commands.Bot(command_prefix='m!', description=description)
voice = None



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello():
    """Says world"""
    await bot.say("world")


@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def echo(message: str):
    """Echoes your message"""
    await bot.say(message)


@bot.command()
async def sendpic(id: int):
    """Will send you a nice pic"""
    file = "../../../../../resources/images/"
    if id <= 2:
        file += "%i.jpg" % id
    else:
        file += "%i.png" % id

    await bot.say("Fetching %s" % file)
    await bot.send_file(bot.get_channel(BRIGITTE_CHANNEL), file)


@bot.command()
async def playmusic(args):
    global voice
    file = "../../../../../resources/music/%s.mp3" % args
    if voice is None:
        voice = await bot.join_voice_channel(bot.get_channel(BRIGITTE_VOICE_CHANNEL))

    if voice.is_connected():
        player = voice.create_ffmpeg_player(file)

        if player.is_done():
            player.stop()
        player.start()


bot.run(TOKEN)
