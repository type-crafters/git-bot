import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class DiscordNotificationBot:
    def __init__(self):
        intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID', '0'))
        self.setup_events()
    
    def setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'🤖 Bot conectado como {self.bot.user}')
            print(f'📢 Canal de notificaciones: {self.channel_id}')
    
    async def send_notification(self, message: str) -> bool:
        """Envía una notificación al canal de Discord"""
        try:
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                await channel.send(message)
                print(f"✅ Notificación enviada a Discord")
                return True
            else:
                print(f"❌ Canal {self.channel_id} no encontrado")
                return False
        except Exception as e:
            print(f"❌ Error al enviar notificación: {str(e)}")
            return False
    
    def format_github_message(self, data: dict) -> str:
        """Formatea un mensaje de commit de GitHub"""
        branch = data['ref'].split('/')[-1]
        repo_name = data['repository']['full_name']
        pusher = data['pusher']['name']
        commits = data['commits']
        
        message = f"🔔 **Nuevo commit en {repo_name}**\n"
        message += f"📂 Branch: `{branch}`\n"
        message += f"👤 Autor: {pusher}\n"
        message += f"📝 Commits ({len(commits)}):\n\n"
        
        for commit in commits[:5]:
            commit_msg = commit['message'].split('\n')[0][:100]
            commit_id = commit['id'][:7]
            author = commit['author']['name']
            message += f"• `{commit_id}` - {commit_msg} ({author})\n"
        
        if len(commits) > 5:
            message += f"\n... y {len(commits) - 5} commits más"
        
        message += f"\n🔗 [Ver cambios]({data['compare']})"
        return message
    
    def format_gitlab_message(self, data: dict) -> str:
        """Formatea un mensaje de commit de GitLab"""
        branch = data['ref'].split('/')[-1]
        repo_name = data['project']['path_with_namespace']
        pusher = data['user_name']
        commits = data['commits']
        
        message = f"🔔 **Nuevo commit en {repo_name}**\n"
        message += f"📂 Branch: `{branch}`\n"
        message += f"👤 Autor: {pusher}\n"
        message += f"📝 Commits ({len(commits)}):\n\n"
        
        for commit in commits[:5]:
            commit_msg = commit['message'].split('\n')[0][:100]
            commit_id = commit['id'][:7]
            author = commit['author']['name']
            message += f"• `{commit_id}` - {commit_msg} ({author})\n"
        
        if len(commits) > 5:
            message += f"\n... y {len(commits) - 5} commits más"
        
        return message
    
    async def start(self):
        """Inicia el bot de Discord"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        if not token:
            raise ValueError("DISCORD_BOT_TOKEN no está configurado")
        
        if self.channel_id == 0:
            print("⚠️ Advertencia: DISCORD_CHANNEL_ID no está configurado")
        
        await self.bot.start(token)
    
    async def close(self):
        """Cierra la conexión del bot"""
        await self.bot.close()

# Instancia global del bot
discord_bot = DiscordNotificationBot()

async def start_bot():
    """Función para iniciar el bot"""
    await discord_bot.start()

if __name__ == '__main__':
    asyncio.run(start_bot())