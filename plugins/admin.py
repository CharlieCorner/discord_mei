import discord.utils
from discord.ext.commands import command

from plugins.plugin import Plugin


class Admin(Plugin):

    @command("changenick", pass_context=True)
    async def on_message(self, ctx, *, message: str):
        print("ok")
        await self.mei.change_nickname(discord.utils.get(ctx.message.server.members, name="mei-ordel"), "mei-ordel")
