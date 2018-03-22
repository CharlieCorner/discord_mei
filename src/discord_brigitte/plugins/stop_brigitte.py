from discord.ext.commands import command
from discord_brigitte.plugins.plugin import Plugin


class StopBrigitte(Plugin):
    @command("stop", pass_context=True)
    async def stop(self, ctx):
        await self.brigitte.say("Stopping, Nowhere to go but up! Bye bye!")
        raise KeyboardInterrupt
