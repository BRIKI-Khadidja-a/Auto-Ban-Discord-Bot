import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PROTECTED_CHANNEL_ID = int(os.getenv("PROTECTED_CHANNEL_ID", 0))
DELETE_WINDOW_SECONDS = int(os.getenv("DELETE_WINDOW_SECONDS", 300))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    print("💬 Bot prêt à surveiller le canal protégé !")

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return

    # Si message dans le canal protégé
    if message.channel.id == PROTECTED_CHANNEL_ID:
        try:
            print(f"🚨 {message.author} a envoyé un message dans le canal protégé.")
            
            # Supprimer les messages récents de cet utilisateur
            async for msg in message.channel.history(limit=100, after=discord.utils.utcnow() - discord.utils.utcnow()):
                if msg.author == message.author:
                    await msg.delete()
            
            # Bannir l'utilisateur
            await message.guild.ban(message.author, reason="Message dans canal protégé")
            print(f"⛔ {message.author} a été banni du serveur.")
        except Exception as e:
            print(f"❌ Erreur lors du ban : {e}")

# Lancer le bot
bot.run(TOKEN)
