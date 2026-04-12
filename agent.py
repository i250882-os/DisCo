import discord
from discord.ext import commands
from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
from tools.channels import *
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
temp  = """
    "name": "create_voice_channel",
    "description": "Creates a voice channel", 
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the channel"
            },
        },
    },
"""

SYSTEM_PROMPT = """
"""
CONTEXT = ""

async def prompt(text, ctx):
    tools = types.Tool(function_declarations=channel_function_declarations)
    config = types.GenerateContentConfig(tools=[tools])
    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=text,
        config=config,
    )
    print(response, "\n\n\n", response.function_calls, "\n\n\n")
    if response.function_calls:
        function_call = response.function_calls[0]
        print(f"Function to call: {function_call.name}")
        print(f"ID: {function_call.id}")
        print(f"Arguments: {function_call.args}")
        if function_call.name == "create_channel":
            await create(ctx)
        #  In a real app, you would call your function here:
        #  result = schedule_meeting(**function_call.args)
    else:
        print("No function call found in the response.")
        print(response.text)
        return response.text

class Listener(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user.mentioned_in(message):
            ctx = await self.bot.get_context(message)
            res = await prompt(message.content, ctx=ctx)
            print(res)
            await message.channel.send(res)

async def setup(bot):
    await bot.add_cog(Listener(bot))
