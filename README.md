# 🤖 Discord Auto-Ban Bot

Un bot Discord qui bannit automatiquement toute personne envoyant un message dans un canal spécifique pour protéger votre serveur contre les spammeurs et les comptes piratés.

## 🎯 Fonctionnalités

- **Surveillance automatique** d'un canal spécifique
- **Bannissement immédiat** des utilisateurs qui postent
- **Nettoyage automatique** des messages des 5 dernières minutes
- **Message d'avertissement** visible dans le canal protégé
- **Statistiques** des actions effectuées
- **Logging complet** de toutes les activités
- **Commandes d'administration** pour gérer le bot

## 🚀 Installation Rapide

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd Auto-Ban-Discord-Bot
```



## 📝 Configuration

### Fichier .env
```env
# Token de votre bot Discord (obligatoire)
DISCORD_TOKEN=your_bot_token_here

# ID du canal à protéger (obligatoire)
PROTECTED_CHANNEL_ID=123456789012345678


```

### Obtenir l'ID d'un canal
1. Activez le mode développeur dans Discord (Paramètres > Avancé > Mode développeur)
2. Clic droit sur le canal > "Copier l'ID"
3. Collez l'ID dans votre fichier `.env`

## 🎮 Utilisation

### Démarrer le bot
```bash
python bot.py
```


