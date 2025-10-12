🎯 Objectif principal

Créer un bot Discord qui bannit automatiquement toute personne envoyant un message dans un canal spécifique (par exemple #no-messages-here).

Le but est de protéger le serveur contre :

Les spammeurs (qui envoient beaucoup de messages ou de pubs)

Les comptes piratés (qui se mettent à spammer sans prévenir)

⚙️ Fonctionnalités principales

Surveillance d’un canal précis
Le bot surveille un canal (ex : #announcements, #bot-control, ou #read-only) défini dans la configuration.

Avertissement visible
Le canal doit contenir un message clair, par exemple :

⚠️ Ne postez aucun message ici — toute personne qui envoie un message sera bannie automatiquement.

Action automatique
Dès qu’un utilisateur envoie un message :

🚫 Le bot bannit immédiatement cet utilisateur.

🗑️ Le bot supprime tous les messages envoyés par cette personne dans les 5 dernières minutes.

Protection du serveur
→ Le but est d’empêcher un utilisateur malveillant ou piraté de nuire avant qu’un modérateur n’intervienne.
