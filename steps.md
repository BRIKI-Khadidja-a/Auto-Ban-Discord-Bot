🧩 Step 1 — Configuration du bot Auto-Ban
🎯 Objectif

Créer un bot Discord capable de bannir automatiquement tout utilisateur qui envoie un message dans un canal protégé.

🪜 Étapes principales

Créer une application Discord sur Discord Developer Portal
 → ajouter un bot et copier le token.

Inviter le bot sur ton serveur via l’onglet OAuth2 → URL Generator, avec les permissions :

Bannir des membres

Gérer les messages

Voir les salons / Envoyer des messages

Créer la structure du projet :

Auto-Ban-Discord-Bot/
├── bot.py
└── .env


Fichier .env :

DISCORD_TOKEN=ton_token_ici
PROTECTED_CHANNEL_ID=ID_DU_CANAL_PROTÉGÉ
DELETE_WINDOW_SECONDS=300


Installer les dépendances :

pip install discord.py python-dotenv


Activer les intents dans le Developer Portal : Presence, Members, Message Content.

Donner les permissions au rôle du bot sur Discord et le placer au-dessus de @everyone.

Lancer le bot :

python bot.py


Tester : lorsqu’un utilisateur envoie un message dans le canal protégé → il est automatiquement banni et ses messages récents sont supprimés.