from discord.ext.commands import command
from discord_mei.plugins.plugin import Plugin


class StopMei(Plugin):
    @command("stop", pass_context=True)
    async def stop(self, ctx):
        await self.mei.say("Stopping, bye bye!")
        raise KeyboardInterrupt
