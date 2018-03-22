from discord.ext.commands import command
from discord_brigitte.plugins.plugin import Plugin


class Echo(Plugin):

    @command("echo", pass_context=True)
    async def on_message(self, ctx, *, message: str):
        await self.brigitte.say("%s to you too %s at %s!" % (message, ctx.message.author.name, ctx.message.channel))

    @command("echo2", pass_context=True)
    async def echo2(self, ctx, *, message: str):
        await self.brigitte.say("No, fuck you!")