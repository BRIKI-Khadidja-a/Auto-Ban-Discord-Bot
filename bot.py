"""
Discord Auto-Ban Bot
Bot qui bannit automatiquement les utilisateurs qui envoient des messages dans un canal protégé.
"""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Charger les variables depuis le fichier .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PROTECTED_CHANNEL_ID = int(os.getenv("PROTECTED_CHANNEL_ID", 0))
DELETE_WINDOW_SECONDS = int(os.getenv("DELETE_WINDOW_SECONDS", 300))

# Vérification des variables obligatoires
if not TOKEN or TOKEN == "your_bot_token_here":
    logger.error("❌ Token Discord manquant ! Vérifiez votre fichier .env")
    exit(1)

if not PROTECTED_CHANNEL_ID or PROTECTED_CHANNEL_ID == 123456789012345678:
    logger.error("❌ ID du canal protégé manquant ! Vérifiez votre fichier .env")
    exit(1)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Statistiques du bot
bot_stats = {
    "bans_count": 0,
    "messages_deleted": 0,
    "last_ban": None
}

@bot.event
async def on_ready():
    logger.info(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    logger.info(f"📊 Servant {len(bot.guilds)} serveur(s)")
    logger.info("💬 Bot prêt à surveiller le canal protégé !")

    # Envoie un message d'avertissement dans le canal protégé
    channel = bot.get_channel(PROTECTED_CHANNEL_ID)
    if channel:
        try:
            embed = discord.Embed(
                title="🚨 CANAL PROTÉGÉ 🚨",
                description="⚠️ **ATTENTION** ⚠️\n\nCe canal est protégé ! Ne postez **AUCUN** message ici.\nToute personne qui envoie un message sera **bannie automatiquement**.\n\n🔒 Canal en lecture seule",
                color=0xff0000
            )
            embed.set_footer(text="Bot de protection automatique")
            embed.timestamp = datetime.utcnow()
            
            await channel.send(embed=embed)
            logger.info("Message d'avertissement posté dans le canal protégé")
        except Exception as e:
            logger.error(f"Erreur lors de la publication du message d'avertissement: {e}")
    else:
        logger.error(f"Canal protégé {PROTECTED_CHANNEL_ID} introuvable")

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return

    # Traiter les commandes
    await bot.process_commands(message)

    # Si message dans le canal protégé
    if message.channel.id == PROTECTED_CHANNEL_ID:
        try:
            logger.warning(f"🚨 {message.author} a envoyé un message dans le canal protégé")
            
            # Supprimer le message immédiatement
            await message.delete()
            logger.info(f"Message supprimé de {message.author}")
            
            # Supprimer les messages récents de cet utilisateur (5 dernières minutes)
            five_minutes_ago = datetime.utcnow() - timedelta(seconds=DELETE_WINDOW_SECONDS)
            deleted_count = 0
            
            async for msg in message.channel.history(limit=100):
                if (msg.author == message.author and 
                    msg.created_at > five_minutes_ago and
                    msg.id != message.id):
                    try:
                        await msg.delete()
                        deleted_count += 1
                        await asyncio.sleep(0.5)  # Éviter le rate limit
                    except:
                        pass
            
            # Bannir l'utilisateur
            ban_reason = f"Message dans canal protégé #{message.channel.name} - Protection automatique"
            await message.guild.ban(message.author, reason=ban_reason, delete_message_days=0)
            logger.warning(f"⛔ {message.author} a été banni du serveur")
            
            # Mettre à jour les statistiques
            bot_stats["bans_count"] += 1
            bot_stats["messages_deleted"] += deleted_count
            bot_stats["last_ban"] = datetime.utcnow().isoformat()
            
            # Envoyer un message de confirmation
            try:
                embed = discord.Embed(
                    title="🔒 Action de Protection",
                    description=f"**{message.author}** a été banni automatiquement pour avoir posté dans ce canal protégé.",
                    color=0xff0000
                )
                embed.add_field(name="Messages supprimés", value=f"{deleted_count}", inline=True)
                embed.add_field(name="Raison", value="Canal protégé", inline=True)
                embed.timestamp = datetime.utcnow()
                
                await message.channel.send(embed=embed, delete_after=10)
            except:
                pass
                
        except discord.Forbidden:
            logger.error("Permissions insuffisantes pour bannir l'utilisateur")
        except Exception as e:
            logger.error(f"Erreur lors du bannissement: {e}")

@bot.command(name="stats")
@commands.has_permissions(administrator=True)
async def show_stats(ctx):
    """Affiche les statistiques du bot"""
    embed = discord.Embed(
        title="📊 Statistiques du Bot de Protection",
        color=0x00ff00
    )
    embed.add_field(name="Bannissements", value=bot_stats["bans_count"], inline=True)
    embed.add_field(name="Messages supprimés", value=bot_stats["messages_deleted"], inline=True)
    embed.add_field(name="Dernier ban", value=bot_stats["last_ban"] or "Aucun", inline=True)
    embed.add_field(name="Canal protégé", value=f"<#{PROTECTED_CHANNEL_ID}>", inline=True)
    embed.timestamp = datetime.utcnow()
    
    await ctx.send(embed=embed)

@bot.command(name="help_ban")
async def help_ban(ctx):
    """Affiche l'aide du bot"""
    embed = discord.Embed(
        title="🤖 Bot de Protection Automatique",
        description="Ce bot protège automatiquement ce canal contre les messages non autorisés.",
        color=0x0099ff
    )
    embed.add_field(
        name="⚠️ Attention",
        value="Ne postez **AUCUN** message dans ce canal ! Vous serez banni automatiquement.",
        inline=False
    )
    embed.add_field(
        name="🔧 Commandes Admin",
        value="`!stats` - Affiche les statistiques",
        inline=False
    )
    embed.set_footer(text="Bot de protection - Canal en lecture seule")
    
    await ctx.send(embed=embed, delete_after=30)

# Gestion des erreurs
@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs de commandes"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Permissions insuffisantes pour utiliser cette commande", delete_after=5)
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignorer les commandes non trouvées
    else:
        logger.error(f"Erreur de commande: {error}")

if __name__ == "__main__":
    logger.info("🚀 Démarrage du bot...")
    bot.run(TOKEN)
