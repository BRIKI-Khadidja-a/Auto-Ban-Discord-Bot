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

### 2. Configuration automatique
```bash
python setup.py
```

### 3. Configuration manuelle
1. Copiez `env_example.txt` vers `.env`
2. Remplissez vos informations dans `.env`
3. Installez les dépendances : `pip install -r requirements.txt`

## ⚙️ Configuration du Bot Discord

### 1. Créer l'application Discord
1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Cliquez sur "New Application"
3. Donnez un nom à votre bot
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. Copiez le **Token** (gardez-le secret !)

### 2. Permissions requises
Votre bot doit avoir ces permissions :
- `BAN_MEMBERS` - Pour bannir les utilisateurs
- `MANAGE_MESSAGES` - Pour supprimer les messages
- `READ_MESSAGE_HISTORY` - Pour lire l'historique
- `SEND_MESSAGES` - Pour envoyer des messages
- `EMBED_LINKS` - Pour les messages avec embed

### 3. Inviter le bot
1. Allez dans l'onglet "OAuth2" > "URL Generator"
2. Cochez "bot" dans les scopes
3. Cochez les permissions listées ci-dessus
4. Copiez l'URL générée et ouvrez-la dans votre navigateur
5. Sélectionnez votre serveur et autorisez le bot

## 📝 Configuration

### Fichier .env
```env
# Token de votre bot Discord (obligatoire)
DISCORD_TOKEN=your_bot_token_here

# ID du canal à protéger (obligatoire)
PROTECTED_CHANNEL_ID=123456789012345678

# Préfixe des commandes (optionnel)
BOT_PREFIX=!

# Message d'avertissement personnalisé (optionnel)
WARNING_MESSAGE=⚠️ **ATTENTION** ⚠️
Ce canal est protégé ! Ne postez **AUCUN** message ici.
Toute personne qui envoie un message sera **bannie automatiquement**.
🔒 Canal en lecture seule
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

### Commandes disponibles
- `!help_ban` - Affiche l'aide du bot
- `!stats` - Affiche les statistiques (Admin uniquement)
- `!warning` - Met à jour le message d'avertissement (Admin uniquement)

## 🔧 Fonctionnement

1. **Surveillance** : Le bot surveille en permanence le canal protégé
2. **Détection** : Dès qu'un message est envoyé dans le canal
3. **Action immédiate** :
   - Suppression du message
   - Bannissement de l'utilisateur
   - Nettoyage des messages des 5 dernières minutes
4. **Logging** : Enregistrement de toutes les actions dans `bot.log`

## 📊 Monitoring

Le bot génère des logs détaillés dans `bot.log` :
- Connexions/déconnexions
- Bannissements effectués
- Messages supprimés
- Erreurs rencontrées

## 🛡️ Sécurité

- **Permissions minimales** : Le bot n'a que les permissions nécessaires
- **Logging complet** : Toutes les actions sont enregistrées
- **Gestion d'erreurs** : Le bot continue de fonctionner même en cas d'erreur
- **Rate limiting** : Protection contre les limites de l'API Discord

## 🚨 Avertissements

⚠️ **Important** : Ce bot bannit **immédiatement** et **sans confirmation** toute personne qui poste dans le canal protégé.

⚠️ **Testez d'abord** : Utilisez un serveur de test avant de déployer en production.

⚠️ **Permissions** : Assurez-vous que le bot a les bonnes permissions et que vous avez le droit de bannir des utilisateurs.

## 📁 Structure du projet

```
Auto-Ban-Discord-Bot/
├── bot.py              # Code principal du bot
├── setup.py            # Script de configuration
├── requirements.txt    # Dépendances Python
├── env_example.txt     # Exemple de configuration
├── README.md           # Documentation
└── bot.log            # Fichier de logs (créé automatiquement)
```

## 🔄 Mise à jour

Pour mettre à jour le bot :
1. Sauvegardez votre fichier `.env`
2. Téléchargez la nouvelle version
3. Remplacez les fichiers (sauf `.env`)
4. Relancez le bot

## 🆘 Support

En cas de problème :
1. Vérifiez les logs dans `bot.log`
2. Vérifiez que le bot a les bonnes permissions
3. Vérifiez que l'ID du canal est correct
4. Vérifiez que le token est valide

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

**Développé avec ❤️ pour protéger vos serveurs Discord**
