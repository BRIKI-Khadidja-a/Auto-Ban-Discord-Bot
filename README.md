
# 🤖 Discord Auto‑Ban Bot

A Discord bot that automatically bans anyone who sends a message in a protected channel. Useful for keeping announcement or verification channels clean and preventing spam or compromised accounts from posting.

## ✨ Features

- **Automatic monitoring** of a specific channel
- **Immediate ban** of users who post in the protected channel
- **Automatic cleanup** of recent messages (last 5 minutes)
- **Warning message** displayed in the protected channel
- **Action statistics** for visibility
- **Full logging** of all moderation actions
- **Admin commands** to manage the bot

---

## 🚀 Quick Start

### 1) Clone the project
```bash
git clone <your-repo-url>
cd Auto-Ban-Discord-Bot
```

### 2) Create a Discord bot and get the token
1. Open the Discord Developer Portal (`https://discord.com/developers/applications`).
2. Create a new Application → add a Bot.
3. Copy the Bot Token and keep it secret.
4. Under Bot → Privileged Gateway Intents, enable the intents your bot needs (usually Server Members).

### 3) Invite the bot to your server
1. In the Developer Portal, go to OAuth2 → URL Generator.
2. Scopes: select `bot`. Permissions: include at least `BAN_MEMBERS`, `VIEW_CHANNEL`, `SEND_MESSAGES`.
3. Copy the generated URL and open it to invite the bot to your server.

### 4) Set up environment variables
Create a `.env` file at the project root:
```env
# Required
DISCORD_TOKEN=your_bot_token_here
PROTECTED_CHANNEL_ID=1427761223117701234
DELETE_WINDOW_SECONDS=300



How to get a channel ID:
1. In Discord, open Settings → Advanced → enable Developer Mode.
2. Right‑click the channel → Copy ID.
3. Paste the ID into `PROTECTED_CHANNEL_ID` in `.env`.

### 5) Create and activate a Python environment (recommended)
```bash
python -m venv .venv
# Windows PowerShell
source .venv/bin/activate
```

### 6) Install dependencies
```bash
pip install -r requirements.txt
```

### 7) Run the bot
```bash
python bot.py
```

---

## ⚙️ Configuration Details

- `DISCORD_TOKEN` (required): Your bot token from the Developer Portal.
- `PROTECTED_CHANNEL_ID` (required): ID of the channel that should be protected.
- `LOG_CHANNEL_ID` (optional): Channel ID where the bot will post logs.
- `CLEANUP_MINUTES` (optional, default 5): How far back to delete messages when cleaning.
- `WARNING_MESSAGE` (optional): Message shown in the protected channel.
- `ADMIN_ROLE_ID` (optional): Role ID allowed to run admin commands.

Make sure the bot’s role has permission to view the protected channel and to ban members.

---


## 🗂️ Logging (Logs)

- This bot uses a **daily rotating log system** (one `.log` file per day) stored in the `logs/` directory at the project root.
- Logs record important actions: connections, detected messages, deletions, bans, and errors.
- The `logs/` directory is created automatically when the bot starts if it does not exist.
- To review logs, navigate to the `logs/` folder and open the current day's log file, for example, `autoban.log`.
- Log rotation ensures log files do not grow too large.

### Why is logging important?

- It facilitates auditing of the bot's automatic actions.
- Useful for troubleshooting errors or unexpected behavior.
- Improves traceability of moderation on your server.


## 🧪 Usage

- When a user posts in the protected channel, the bot will ban them and optionally delete recent messages.
- The bot can post a warning message in the channel so users know not to post there.
- If admin commands are implemented, ensure your admin role is set via `ADMIN_ROLE_ID`.

Common admin tasks (examples):
- Show current settings
- Toggle cleanup or change cleanup minutes
- Update the warning message

Refer to your command list (slash or prefix) if available in the code.

---

## 🔐 Permissions & Intents

- Intents: enable the intents required by your implementation (commonly Server Members).
- Permissions: the bot should have `BAN_MEMBERS`, `VIEW_CHANNEL`, and `SEND_MESSAGES`. Grant only what is necessary.

---

## 🛠️ Troubleshooting

- Bot offline
  - Check `DISCORD_TOKEN` and that the token is valid.
  - Confirm required intents are enabled in the Developer Portal.
  - Review console logs for exceptions on startup.
- Ban not working
  - Ensure the bot’s role is above the target user’s role.
  - Confirm the bot has `BAN_MEMBERS` permission in the server.
  - Verify `PROTECTED_CHANNEL_ID` is correct and the bot can read the channel.
- Channel ID not found
  - Make sure Developer Mode is enabled and you copied the correct ID.

---


## 📝 THANK YOU



