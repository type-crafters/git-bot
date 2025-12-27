import discord
import os
from discord import Guild, TextChannel
from discord.ext.commands import Bot
from dotenv import load_dotenv
from lib import use_markdown
from typing import Optional

load_dotenv()

class DiscordNotificationBot:
    __bot: Bot

    @property
    def bot(self) -> Bot:
        return self.__bot

    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        self.__bot = Bot(command_prefix='!', intents=intents)

        @self.__bot.event
        async def on_ready(self):
            user = self.__bot.user
            print(f"🤖 Bot conectado como {user} (ID: {user.id})")

        @self.__bot.event
        async def on_guild_join(self, guild: Guild):
            if (channel := self.__get_default_channel(guild)) is not None:
                await channel.send(use_markdown('Welcome.md'))

    def __get_default_channel(guild: Guild) -> Optional[TextChannel]:
        if (sysch := guild.system_channel):
            if sysch.permissions_for(guild.me).send_messages:
                return sysch
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel
        return None

    async def start(self):
        """
        Inicia el bot de Discord
        """
        if (token := os.getenv('BOT_TOKEN')) is None:
            raise ValueError('Hace falta la variable de entorno \'BOT_TOKEN\'.')
        await self.__bot.start(token)

    async def close(self):
        """
        Cierra la conexión del bot
        """
        await self.__bot.close()

