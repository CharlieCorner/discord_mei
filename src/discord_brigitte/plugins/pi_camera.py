try:
    import picamera
    IS_PICAMERA_SUPPORTED = True
except ImportError:
    IS_PICAMERA_SUPPORTED = False


from discord.ext.commands import command
from discord_brigitte.plugins.plugin import Plugin


class PiCamera(Plugin):

    @command("take_pi_pic", pass_context=True)
    async def on_message(self, ctx):
        """Take a pic from the Pi camera!"""

        file = "../../resources/images/cheese.jpg"

        if not IS_PICAMERA_SUPPORTED:
            await self.brigitte.say("No Pi Camera module is installed :cry:")
            return
        else:
            with picamera.PiCamera() as camera:
                camera.capture(file)

            await self.brigitte.say("Yay! It is supported!")
            await self.brigitte.send_file(ctx.message.channel, file)
