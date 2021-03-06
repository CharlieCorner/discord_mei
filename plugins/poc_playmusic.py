from discord.ext.commands import command

from plugins.plugin import Plugin


class PocPlayMusic(Plugin):

    def __init__(self, *args):
        super().__init__(*args)
        self.voice = None

    @command("playmusic")
    async def on_message(self, song_id: str):

        file = "../../resources/music/%s.mp3" % song_id

        if self.voice is None:
            self.voice = await self.mei.join_voice_channel(self.mei.get_channel(self.mei.voice_channel_id))

        if self.voice.is_connected():
            player = self.voice.create_ffmpeg_player(file)

            if player.is_done():
                player.stop()
            player.start()