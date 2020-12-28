import logging

import pyaudio
from discord.ext import commands
from discord.opus import Encoder as OpusEncoder

LOGGER = logging.getLogger("discord_mei.%s" % __name__)


class Security(commands.Cog):

    CHUNK = 1024
    WIDTH = 2
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 7

    def __init__(self, bot):
        self.bot = bot
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None

    @commands.command()
    @commands.is_owner()
    async def mic(self, ctx):

        def send_data_to_channel(in_data, frame_count, time_info, status):

            ctx.voice_client.send_audio_packet(in_data, encode=True)

            return in_data, pyaudio.paContinue

        async with ctx.typing():

            self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(Security.WIDTH),
                                            channels=OpusEncoder.CHANNELS,
                                            rate=OpusEncoder.SAMPLING_RATE,
                                            input=True,
                                            output=False,
                                            frames_per_buffer=OpusEncoder.SAMPLES_PER_FRAME,
                                            stream_callback=send_data_to_channel,
                                            start=False
                                            )

        LOGGER.info("About to send stream to channel...")
        self.stream.start_stream()
        # ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now streaming on voice channel: {}'.format(ctx.voice_client.channel.name))
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def stop_mic(self, ctx):

        await ctx.message.delete()

        await self._stop_stream(ctx, notify_on_no_stream=True)

    async def _stop_stream(self, ctx, notify_on_no_stream: bool = False):

        if self.stream and self.stream.is_active():
            LOGGER.info("Stopping stream...")
            await ctx.send(f"Stopping stream in channel {ctx.voice_client.channel.name}...", delete_after=15)

            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

            LOGGER.info("Disconnecting bot from voice channel...")
            await ctx.voice_client.disconnect()

        else:
            if notify_on_no_stream:
                await ctx.send("No stream is currently active!", delete_after=10)

    @mic.before_invoke
    async def invoking_validation(self, ctx):

        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if not ctx.voice_client.encoder:
            ctx.voice_client.encoder = OpusEncoder()

        await self._stop_stream(ctx)

