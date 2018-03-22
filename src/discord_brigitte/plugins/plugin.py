import logging

import discord

LOGGER = logging.getLogger("discord_brigitte.%s" % __name__)


class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""

        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class Plugin(metaclass=PluginMount):

    def __init__(self, brigitte):
        self.brigitte = brigitte
        self.commands = None

    def get_commands(self):

        if self.commands is not None:
            return self.commands

        commands = []
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)

            if isinstance(attribute, discord.ext.commands.core.Command):
                commands.append(attribute)
        self.commands = commands
        return self.commands

    async def on_ready(self):
        pass

    async def _on_message(self, message):
        for command_name, func in self.commands.items():
            await func(message)
        await self.on_message(message)

    async def on_message(self, message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_message_delete(self, message):
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_server_join(self, server):
        pass

    async def on_server_update(self, before, after):
        pass

    async def on_server_role_create(self, server, role):
        pass

    async def on_server_role_delete(self, server, role):
        pass

    async def on_server_role_update(self, server, role):
        pass

    async def on_voice_state_update(self, before, after):
        pass

    async def on_member_ban(self, member):
        pass

    async def on_member_unban(self, member):
        pass

    async def on_typing(self, channel, user, when):
        pass