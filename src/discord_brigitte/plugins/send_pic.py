import os.path

from discord.ext.commands import command
from discord_brigitte.plugins.plugin import Plugin

class SendPic(Plugin):

    @command("sendpic", pass_context=True)
    async def on_message(self, ctx, id: int):
        """Will send you a nice pic"""
        file = "../../resources/images/"
        if id <= 2:
            file += "%i.jpg" % id
        else:
            file += "%i.png" % id

        if not os.path.isfile(file):
            return await self.brigitte.say("%s doesn't exist bucko!" % file)

        await self.brigitte.say("Fetching %s" % file)
        await self.brigitte.send_file(ctx.message.channel, file)
