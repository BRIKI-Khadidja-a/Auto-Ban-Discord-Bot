"""
Discord Auto-Ban Bot 
Bot qui bannit automatiquement les utilisateurs postant dans un canal protégé :
- Supprime immédiatement le message
- Bannit automatiquement (sauf admins)
- Nettoie les messages récents
- Empêche le retour des bannis
"""
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import logging
from logging.handlers import TimedRotatingFileHandler


# === CONFIGURATION LOGGING ===
logger = logging.getLogger("AutoBanBot")
logger.setLevel(logging.INFO)
os.makedirs("logs", exist_ok=True)
handler = TimedRotatingFileHandler("logs/autoban.log", when="midnight", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


# === CHARGEMENT .env ===
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PROTECTED_CHANNEL_ID = int(os.getenv("PROTECTED_CHANNEL_ID", 0))
DELETE_WINDOW_SECONDS = int(os.getenv("DELETE_WINDOW_SECONDS", 300))


if not TOKEN:
    logger.error("❌ Token Discord manquant dans .env !")
    exit(1)
if not PROTECTED_CHANNEL_ID:
    logger.error("❌ ID du canal protégé manquant dans .env !")
    exit(1)


# === INTENTS DISCORD ===
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True


bot = commands.Bot(command_prefix="!", intents=intents)
bot_stats = {"bans_count": 0, "messages_deleted": 0, "last_ban": None}


# === MESSAGE D'AVERTISSEMENT EMBED ===
def get_protection_embed():
    embed = discord.Embed(
        title="🪧 CANAL PROTÉGÉ 🪧",
        description="⚠️ **ATTENTION** ⚠️\n\nCe canal est protégé ! Ne postez **AUCUN** message ici.\nToute personne qui envoie un message sera **bannie automatiquement**.",
        color=0xff0000,
        timestamp=datetime.now(timezone.utc)
    )
    embed.add_field(
        name="📙 Canal en lecture seule",
        value="",
        inline=False
    )
    embed.add_field(
        name="**Nouvelles personnes :**",
        value="Vous pouvez rejoindre le serveur, mais ne postez pas ici !",
        inline=False
    )
    embed.add_field(
        name="🛡️ Protection Active",
        value="• Bannissement immédiat si message\n• Nettoyage des messages (5 min)\n• Vérification des retours de bannis",
        inline=False
    )
    embed.set_footer(text="Bot de protection automatique • Serveur sécurisé")
    return embed


# === ÉVÉNEMENT DE CONNEXION ===
@bot.event
async def on_ready():
    logger.info(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    channel = bot.get_channel(PROTECTED_CHANNEL_ID)
    if not channel:
        logger.error("❌ Canal protégé introuvable")
        return
    await channel.send(embed=get_protection_embed())
    logger.info("✅ Message d’avertissement affiché")


# === SURVEILLANCE DU CANAL ===
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    if message.channel.id != PROTECTED_CHANNEL_ID:
        return


    logger.warning(f"🚨 Message détecté dans le canal protégé par {message.author}")
    if not message.guild.me.guild_permissions.ban_members:
        logger.error("❌ Permissions insuffisantes pour bannir")
        return
    if message.author.top_role >= message.guild.me.top_role:
        logger.warning("❌ L'auteur a un rôle supérieur ou égal : pas de bannissement")
        try:
            await message.delete()
        except:
            pass
        return


    # SUPPRESSION IMMEDIATE DU MESSAGE
    try:
        await message.delete()
        logger.info(f"✅ Message supprimé de {message.author}")
    except Exception as e:
        logger.error(f"Erreur suppression message : {e}")


    # SUPPRESSION MESSAGES RÉCENTS
    five_minutes_ago = datetime.now(timezone.utc) - timedelta(seconds=DELETE_WINDOW_SECONDS)
    deleted_count = 0
    try:
        async for msg in message.channel.history(limit=100):
            if (msg.author == message.author and msg.created_at > five_minutes_ago):
                try:
                    await msg.delete()
                    deleted_count += 1
                    await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"Erreur suppression historique : {e}")
        if deleted_count > 0:
            logger.info(f"✅ {deleted_count} messages supprimés de {message.author}")
    except Exception as e:
        logger.error(f"Erreur durant le nettoyage : {e}")


    # BANNISSEMENT
    try:
        ban_reason = f"Message dans canal protégé #{message.channel.name}"
        await message.guild.ban(message.author, reason=ban_reason, delete_message_seconds=0)
        bot_stats["bans_count"] += 1
        bot_stats["messages_deleted"] += deleted_count
        bot_stats["last_ban"] = datetime.now(timezone.utc).isoformat()


        embed = discord.Embed(
            title="🔒 Utilisateur banni automatiquement",
            description=f"{message.author} a violé la protection du canal.",
            color=0xff0000,
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Messages supprimés", value=str(deleted_count))
        await message.channel.send(embed=embed, delete_after=10)
        logger.warning(f"⛔ {message.author} banni du serveur")
    except discord.Forbidden:
        logger.error("❌ Interdiction du serveur : hiérarchie ou permissions invalides")
    except Exception as e:
        logger.error(f"Erreur bannissement : {e}")


# === SURVEILLANCE REJOINT MEMBRES BANNNIS ===
@bot.event
async def on_member_join(member):
    logger.info(f"👋 Member joined: {member} (ID: {member.id})")  # Log affichage ajoutée
    

    banned_ids = [b.user.id async for b in member.guild.bans()]
    if member.id in banned_ids:
        await member.guild.ban(member, reason="Tentative de retour après bannissement")
        logger.warning(f"🚫 {member} re-banni à la reconnexion")
    else:
        logger.info(f"👋 Nouveau membre autorisé : {member}")


# === COMMANDES ADMIN ===
@bot.command(name="stats")
@commands.has_permissions(administrator=True)
async def show_stats(ctx):
    embed = discord.Embed(title="📊 Statistiques", color=0x00ff00)
    embed.add_field(name="Bannissements", value=bot_stats["bans_count"])
    embed.add_field(name="Messages supprimés", value=bot_stats["messages_deleted"])
    embed.add_field(name="Dernier ban", value=bot_stats["last_ban"] or "Aucun")
    await ctx.send(embed=embed)


# === LANCEMENT ===
if __name__ == "__main__":
    logger.info("🚀 Démarrage du bot...")
    bot.run(TOKEN)
