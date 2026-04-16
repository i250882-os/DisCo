# DisCo

DisCo is a Discord server administration bot powered by AI LLM. Its a co-pilot for your discord server, the aim for this project is to make it good enough that you only need one manager in your discord server, this bot.

## Features
- Create public/private channels
- Create nsfw and voice channels
- Create channel categories
- Move channel into categories
- Move categories around
- Move channels around inside a category 
- Edit Text and Voice channel settings like:
   - Bitrate for voice channels
   - RTC region for voice channels
   - Toggle Nsfw
   - Change Name
   - Change channel topic

## Requirements
- Discord bot token
- Gemini API key

## Setup
1. Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_KEY=your_gemini_api_key
BOT_ID=you_discord_bot_user_id
```

2. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the bot:

```bash
python bot.py
```

## How It Works
- Start by running the `/initialize` command
- The bot listens for messages in the configured `ai-chat` channel or when mentioned.
- Only the server owner can interact with it.
- Read only operations can run immediately.
- Any action that creates, edits, or deletes server resources requires explicit confirmation.

## License
MIT
