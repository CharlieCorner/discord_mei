from discord.ext.commands import command

from plugins.plugin import Plugin


class StopMei(Plugin):
    @command("stop", pass_context=True)
    async def stop(self, ctx):
        await self.mei.say("Stopping, Nowhere to go but up! Bye bye!")
        raise KeyboardInterrupt
