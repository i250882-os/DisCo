import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from database import init_database, check_initialized, initialize_guild
from logs import logger

TESTING_ENV_ID = 1492924434569236701

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    guild = discord.Object(id=TESTING_ENV_ID)
    synced = await bot.tree.sync(guild=guild)
    print(f"Synced commands: {len(synced)}")
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print(f"Intents: {bot.intents.message_content}")


@bot.tree.command(
    name="initialize",
    description="First thing to do after adding the bot",
    guild=discord.Object(id=TESTING_ENV_ID),
)
async def init(interaction: discord.Interaction):
    exists = check_initialized(interaction.guild_id)
    logger.debug(f"DEBUG: Return in init {exists}")
    if not interaction.guild:
        await interaction.response.send_message("Please run the command in a Server")
    elif exists:
        await interaction.response.send_message("Server Already Initialized")
    else:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),
        }
        ai_channel = await interaction.guild.create_text_channel(
            name="ai-chat", reason="Initialized Command", overwrites=overwrites
        )
        log_channel = await interaction.guild.create_text_channel(
            name="ai-logs", reason="Initialized Command", overwrites=overwrites
        )
        res = initialize_guild(
            guild_id=interaction.guild_id,
            log_channel_id=log_channel.id,
            ai_channel_id=ai_channel.id,
        )
        print(res["message"])
        await interaction.response.send_message(res["message"])


async def main():
    async with bot:
        await bot.load_extension("agent")
        print("Loaded Extensions")
        await bot.start(DISCORD_TOKEN)


import traceback

if __name__ == "__main__":
    init_database()
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\033[31m EXCEPTION in Prompt: {type(e).__name__}: {e}")
        traceback.print_exc()
