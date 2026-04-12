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

TOOLS = channel_function_map

SYSTEM_PROMPT = """
"""
CONTEXT = """
"""

async def execute_tool(ctx, name, args):
    func = TOOLS[name]
    print("DEBUG: Tool Execution of", name, func, "Args", args)
    res = await func(ctx, **args)
    print("DEBUG: Tool Retrun", name, res)
    if res:
        return {"status": "success", "response": res}
    else:
        return {"status": "failed"}

tools = types.Tool(function_declarations=channel_function_declarations)
config = types.GenerateContentConfig(tools=[tools])
client = genai.Client(api_key=GEMINI_KEY)
 
async def prompt(ctx, text):
    messages = [{"role": "user", "parts": [{"text": text}]}]
    
    while True:
        print("DEBUG: Agentic Loop Iteration")
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=messages,
            config=config,
        )

        if not response.candidates or not response.candidates[0].content or not response.candidates[0].content.parts:
            return "No response from model"
        part = response.candidates[0].content.parts[0]

        if response.function_calls:
            function_call = response.function_calls[0]
            name = function_call.name
            args = {}
            if function_call.args:
                args = {k: v for k, v in function_call.args.items()}

            print("\n\nDEBUG: PRINTING THOUGHTS", part.text)
            print(f"Function to call: {function_call.name}")
            print(f"ID: {function_call.id}")
            print(f"Arguments: {function_call.args}")
            results = await execute_tool(ctx, name, args)
            
            messages.append({"role":"model", "parts": [part]})
            messages.append({
                "role": "user",
                "parts": [types.Part(function_response=types.FunctionResponse(name=name, response=results))]
            })
        else:
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
            res = await prompt(ctx, message.content)
            print("DEBUG: Return value of Prompt", res)
            await message.channel.send(res)

async def setup(bot):
    await bot.add_cog(Listener(bot))
