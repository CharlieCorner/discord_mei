import logging

import numpy as np
import pyaudio
from discord import Member, VoiceState, VoiceChannel
from discord.ext import commands
from discord.opus import Encoder as OpusEncoder

LOGGER = logging.getLogger("discord_mei.%s" % __name__)


class Security(commands.Cog):

    MIC_CHANNELS = 1
    WIDTH = 2
    DEFAULT_VOLUME = 100

    def __init__(self, bot):
        self.bot = bot
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        self.custom_encoder = CustomizableOpusEncoder(channels=Security.MIC_CHANNELS)
        self.volume = Security.DEFAULT_VOLUME
        self.active_voice_channel = None

        # Add event listeners
        self.bot.add_listener(self.on_voice_state_update)

    @commands.command()
    @commands.is_owner()
    async def mic(self, ctx):
        """
        Start streaming from a hardware microphone in the voice chat in which the owner is currently connected
        """

        def send_data_to_channel(in_data, frame_count, time_info, status):

            # Set the volume level by transforming the data to a numpy array
            sound_level = (self.volume / 100.)

            chunk = np.fromstring(in_data, np.int16) * sound_level
            chunk = chunk.astype(np.int16)

            ctx.voice_client.send_audio_packet(chunk.tobytes(), encode=True)

            return in_data, pyaudio.paContinue

        async with ctx.typing():

            self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(Security.WIDTH),
                                            channels=self.custom_encoder.CHANNELS,
                                            rate=self.custom_encoder.SAMPLING_RATE,
                                            input=True,
                                            output=False,
                                            frames_per_buffer=self.custom_encoder.SAMPLES_PER_FRAME,
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
    async def volume(self, ctx, new_volume: int):
        """
        Controls the volume of the stream it should be a value [1-200]
        """
        # Volume should be between 1-200
        new_volume = max(min(200, new_volume), 10)

        await ctx.message.delete()
        self.volume = new_volume

        await ctx.send("Setting the volume to: {}".format(new_volume), delete_after=10)

    @commands.command(aliases=["mic_stop"])
    @commands.is_owner()
    async def stop_mic(self, ctx):
        """Stops the stream of the microphone (if there is any one active)"""

        await ctx.message.delete()

        await self._disconnect_stream(ctx, notify_on_no_stream=True)

    def _stop_and_reset_stream_state(self):
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.active_voice_channel = None

        self.volume = Security.DEFAULT_VOLUME

    async def _disconnect_stream(self, ctx, notify_on_no_stream: bool = False):

        if self.stream and self.stream.is_active():
            LOGGER.info("Stopping stream...")
            await ctx.send("Stopping stream in channel {}...".format(ctx.voice_client.channel.name), delete_after=15)

            self._stop_and_reset_stream_state()

            LOGGER.info("Disconnecting bot from voice channel...")
            await ctx.voice_client.disconnect()

        else:
            if notify_on_no_stream:
                await ctx.send("No stream is currently active!", delete_after=10)

    async def _connect_to_author_voice_channel(self, ctx):
        if ctx.author.voice:
            self.active_voice_channel = ctx.author.voice.channel
            await self.active_voice_channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")

    @mic.before_invoke
    async def invoking_validation(self, ctx):
        """A stream can only proceed if it is connected to a voice channel and a stream is not active."""

        if ctx.voice_client is None:
            LOGGER.info("{} is not connected to a voice channel, connecting to {}'s channel...".format(
                self.bot.user.name,
                ctx.author.name))

        elif ctx.voice_client.is_playing() or (self.stream and self.stream.is_active()):
            LOGGER.info("A stream was already playing, resetting and reconnecting to {}'s channel".format(
                ctx.author.name))
            # Reset the stream to move to wherever the author is (if they are)

            ctx.voice_client.stop()
            await self._disconnect_stream(ctx)

        await self._connect_to_author_voice_channel(ctx)

        # Make sure that the Opus encoder is always a Customizable one
        if not ctx.voice_client.encoder or not isinstance(ctx.voice_client.encoder, CustomizableOpusEncoder):
            ctx.voice_client.encoder = self.custom_encoder

    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        """Check if the bot is the only one left in the voice channel, if it is, disconnect it"""

        LOGGER.debug("Got on_voice_state_update!!")

        if not self.active_voice_channel:
            LOGGER.debug("No active voice channel!")
            return

        b4_channel = before.channel
        active_voice_id = self.active_voice_channel.id

        conditions_to_disconnect = [self._is_bot_alone_in_channel(self.active_voice_channel),
                                    (self.stream and self.stream.is_active),
                                    (b4_channel and active_voice_id == b4_channel.id),
                                    ]

        LOGGER.debug("Checking if we should disconnect with: {}".format(conditions_to_disconnect))

        if all(conditions_to_disconnect):

            LOGGER.info("Auto-disconnecting bot from voice channel, it was alone in channel {} :(...".format(
                self.active_voice_channel.name))

            self._stop_and_reset_stream_state()

            for vc in self.bot.voice_clients:
                if vc.channel.id == active_voice_id:
                    LOGGER.debug("Disconnecting from channel {}".format(vc.channel.id))
                    await vc.disconnect()

            self.active_voice_channel = None

    def _is_bot_alone_in_channel(self, voice_channel: VoiceChannel):
        num_connected_members = len(voice_channel.members)

        if num_connected_members >= 2:
            return False
        else:
            if num_connected_members == 0:
                return True
            else:
                lonely_member = voice_channel.members[0]

                return lonely_member.id == self.bot.user.id


class CustomizableOpusEncoder(OpusEncoder):

    BIT_RATE = 16   # This is the bitrate that Discord.py uses by default for the calculation of the sample_size

    def __init__(self,
                 sampling_rate: int = OpusEncoder.SAMPLING_RATE,
                 channels: int = OpusEncoder.CHANNELS,
                 frame_length: int = OpusEncoder.FRAME_LENGTH
                 ):

        self.SAMPLING_RATE = sampling_rate
        self.CHANNELS = channels
        self.FRAME_LENGTH = frame_length

        # Dependant variables
        self.SAMPLE_SIZE = int(self.BIT_RATE / 8) * self.CHANNELS
        self.SAMPLES_PER_FRAME = int(self.SAMPLING_RATE / 1000 * self.FRAME_LENGTH)
        self.FRAME_SIZE = self.SAMPLES_PER_FRAME * self.SAMPLE_SIZE

        # Let the original encoder continue with the configuration
        super().__init__()
