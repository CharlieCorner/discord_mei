from discord.ext.commands import command

from plugins.plugin import Plugin


class Echo(Plugin):

    @command("echo", pass_context=True)
    async def on_message(self, ctx, *, message: str):
        await self.mei.say("%s to you too %s at %s!" % (message, ctx.message.author.name, ctx.message.channel))

    @command("echo2", pass_context=True)
    async def echo2(self, ctx, *, message: str):
        await self.mei.say("No, fuck you!")