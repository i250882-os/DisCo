import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()
DISCORD_TOKEN= os.getenv('DISCORD_TOKEN', "")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print(f"Intents: {bot.intents.message_content}")

async def main():
    async with bot:
        await bot.load_extension("agent")
        print("Loaded Extensions")
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())
