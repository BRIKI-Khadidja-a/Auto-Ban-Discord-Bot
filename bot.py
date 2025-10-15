"""
Discord Auto-Ban Bot
Bot qui bannit automatiquement les utilisateurs qui envoient des messages dans un canal protégé.
- Bannit immédiatement quiconque poste dans le canal spécifié
- Empêche les personnes bannies de revenir
- Nettoie automatiquement les messages des 5 dernières minutes
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
    logger.info("🛡️ Bot prêt à surveiller le canal protégé !")
    logger.info("🔒 Protection active : Bannissement automatique + Vérification des retours")

    # Envoie un message d'avertissement dans le canal protégé
    channel = bot.get_channel(PROTECTED_CHANNEL_ID)
    if channel:
        try:
            embed = discord.Embed(
                title="🚨 CANAL PROTÉGÉ 🚨",
                description="⚠️ **ATTENTION** ⚠️\n\nCe canal est protégé ! Ne postez **AUCUN** message ici.\nToute personne qui envoie un message sera **bannie automatiquement**.\n\n🔒 Canal en lecture seule\n\n**Nouvelles personnes :** Vous pouvez rejoindre le serveur, mais ne postez pas ici !",
                color=0xff0000
            )
            embed.add_field(
                name="🛡️ Protection Active",
                value="• Bannissement immédiat si message\n• Nettoyage des messages (5 min)\n• Vérification des retours de bannis",
                inline=False
            )
            embed.set_footer(text="Bot de protection automatique • Serveur sécurisé")
            embed.timestamp = datetime.utcnow()
            
            await channel.send(embed=embed)
            logger.info("✅ Message d'avertissement posté dans le canal protégé")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la publication du message d'avertissement: {e}")
    else:
        logger.error(f"❌ Canal protégé {PROTECTED_CHANNEL_ID} introuvable")

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-même
    if message.author == bot.user:
        return

    # Traiter les commandes
    await bot.process_commands(message)

    # Si message dans le canal protégé
    if message.channel.id == PROTECTED_CHANNEL_ID:
        logger.info(f"🔍 Message détecté dans le canal protégé par {message.author}")
        try:
            logger.warning(f"🚨 {message.author} a envoyé un message dans le canal protégé")
            
            # Supprimer le message immédiatement
            try:
                await message.delete()
                logger.info(f"✅ Message supprimé de {message.author}")
            except Exception as e:
                logger.error(f"❌ Erreur lors de la suppression du message: {e}")
            
            # Supprimer les messages récents de cet utilisateur (5 dernières minutes)
            five_minutes_ago = datetime.utcnow() - timedelta(seconds=DELETE_WINDOW_SECONDS)
            deleted_count = 0
            
            try:
                async for msg in message.channel.history(limit=100):
                    if (msg.author == message.author and 
                        msg.created_at > five_minutes_ago and
                        msg.id != message.id):
                        try:
                            await msg.delete()
                            deleted_count += 1
                            await asyncio.sleep(0.5)  # Éviter le rate limit
                        except Exception as e:
                            logger.error(f"❌ Erreur suppression message {msg.id}: {e}")
                logger.info(f"✅ {deleted_count} messages supprimés de {message.author}")
            except Exception as e:
                logger.error(f"❌ Erreur lors du nettoyage des messages: {e}")
            
            # Bannir l'utilisateur
            try:
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
                except Exception as e:
                    logger.error(f"❌ Erreur envoi message confirmation: {e}")
                    
            except discord.Forbidden:
                logger.error("❌ Permissions insuffisantes pour bannir l'utilisateur")
            except Exception as e:
                logger.error(f"❌ Erreur lors du bannissement: {e}")
                
        except Exception as e:
            logger.error(f"❌ Erreur générale dans la protection: {e}")

@bot.event
async def on_member_join(member):
    """Événement déclenché quand quelqu'un rejoint le serveur"""
    logger.info(f"👋 Nouveau membre: {member} (ID: {member.id})")
    
    # Vérifier si cette personne était bannie auparavant
    try:
        # Vérifier si l'utilisateur est dans la liste des bannis
        ban_entry = await member.guild.fetch_ban(member)
        if ban_entry:
            logger.warning(f"🚨 TENTATIVE DE RETOUR: {member} était banni et essaie de revenir!")
            
            # Re-bannir immédiatement
            ban_reason = f"Tentative de retour après bannissement - Protection automatique"
            await member.guild.ban(member, reason=ban_reason, delete_message_days=0)
            logger.warning(f"⛔ {member} re-banni automatiquement")
            
            # Envoyer un message d'alerte dans le canal protégé
            channel = bot.get_channel(PROTECTED_CHANNEL_ID)
            if channel:
                try:
                    embed = discord.Embed(
                        title="🚨 TENTATIVE DE RETOUR DÉTECTÉE",
                        description=f"**{member}** a tenté de revenir après avoir été banni.\n\n**Action :** Re-banni automatiquement",
                        color=0xff0000
                    )
                    embed.add_field(name="Raison", value="Tentative de retour après bannissement", inline=True)
                    embed.add_field(name="Protection", value="Active", inline=True)
                    embed.timestamp = datetime.utcnow()
                    embed.set_footer(text="Protection automatique • Retour de banni")
                    
                    await channel.send(embed=embed, delete_after=30)
                except:
                    pass
                    
    except discord.NotFound:
        # L'utilisateur n'était pas banni, c'est un nouveau membre normal
        logger.info(f"✅ Nouveau membre autorisé: {member}")
        
        # Envoyer un message de bienvenue dans le canal protégé
        channel = bot.get_channel(PROTECTED_CHANNEL_ID)
        if channel:
            try:
                embed = discord.Embed(
                    title="👋 Nouveau Membre",
                    description=f"**{member}** a rejoint le serveur.\n\n⚠️ **Rappel :** Ne postez pas dans ce canal !",
                    color=0x00ff00
                )
                embed.add_field(
                    name="📋 Règles",
                    value="• Ce canal est en lecture seule\n• Tout message = bannissement\n• Respectez les règles du serveur",
                    inline=False
                )
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text="Bienvenue • Serveur protégé")
                
                await channel.send(embed=embed, delete_after=60)
            except:
                pass
                
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification du nouveau membre: {e}")

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
        description="Ce bot protège automatiquement ce canal contre les messages non autorisés et gère les retours de bannis.",
        color=0x0099ff
    )
    embed.add_field(
        name="⚠️ RÈGLES IMPORTANTES",
        value="• **NE POSTEZ PAS** dans ce canal !\n• Tout message = **BANNISSEMENT IMMÉDIAT**\n• Les bannis ne peuvent **PAS** revenir",
        inline=False
    )
    embed.add_field(
        name="🛡️ Protection Active",
        value="• Bannissement automatique des messages\n• Nettoyage des messages (5 dernières minutes)\n• Détection des retours de bannis\n• Re-bannissement automatique",
        inline=False
    )
    embed.add_field(
        name="👋 Nouveaux Membres",
        value="• Vous pouvez rejoindre le serveur\n• Respectez les règles\n• Ce canal est en lecture seule",
        inline=False
    )
    embed.add_field(
        name="🔧 Commandes Admin",
        value="`!stats` - Affiche les statistiques",
        inline=False
    )
    embed.set_footer(text="Serveur protégé • Canal en lecture seule")
    
    await ctx.send(embed=embed, delete_after=45)

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