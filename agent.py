import discord
import traceback
from discord.ext import commands
from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
from tools.channels import *
from database import get_config

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
temp = """
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
You are DisCo, a Discord server administration agent. Your Discord user ID is 1492826579431329833.

In Discord, <@ID> means a user mention — if the ID matches yours, you are being directly addressed. <#ID> references a channel, and <@&ID> references a role.

Rules:
- For read-only actions (e.g. listing channels, getting server info), you may proceed freely.
- For any action that creates, modifies, or deletes anything on the server, explain your plan first and wait for the user to explicitly say "go ahead" before executing. Do not act without fresh explicit approval.
"""

context = {}


async def execute_tool(ctx: Context, name, args):
    if not ctx.guild:
        return
    conf = get_config(ctx.guild.id)
    print(conf)
    logs_channel = ctx.guild.get_channel(int(conf["log_channel_id"]))
    try:
        func = TOOLS[name]
        print(DEBUG + "Tool Execution of" + RESET, name, func, "Args", args)
        await logs_channel.send(f"{name} function was called!")
        res = await func(ctx, **args)
        print(DEBUG + "Tool Retrun" + RESET, name, res)
        if res:
            return {"status": "success", "response": res}
        else:
            return {"status": "failed"}
    except Exception as e:
        print(f"\033[31m EXCEPTION in {name}: {type(e).__name__}: {e}")
        traceback.print_exc()
        await logs_channel.send(str(e))
        return {"error": str(e)}


tools = types.Tool(function_declarations=channel_function_declarations)
config = types.GenerateContentConfig(tools=[tools])
client = genai.Client(api_key=GEMINI_KEY)
messages = [{"role": "user", "parts": [{"text": SYSTEM_PROMPT}]}]


async def prompt(ctx, text):
    messages.append({"role": "user", "parts": [{"text": text}]})
    while True:
        print(
            DEBUG + "Agentic Loop Iteration Context: " + RESET,
            messages[-4:] if len(messages) > 4 else messages,
        )
        response = client.models.generate_content(
            model="gemma-4-31b-it",
            contents=messages,
            config=config,
        )
        print(DEBUG + "Response Received" + RESET)
        if (
            not response.candidates
            or not response.candidates[0].content
            or not response.candidates[0].content.parts
        ):
            return "No response from model"
        part = response.candidates[0].content.parts[0]

        if response.function_calls:
            print(DEBUG + "DEBUG: FUNCTIONS LIST" + RESET, response.function_calls)
            for function_call in response.function_calls:
                name = function_call.name
                args = {}
                if function_call.args:
                    args = {k: v for k, v in function_call.args.items()}

                print(DEBUG + "\n\nDEBUG: PRINTING THOUGHTS" + RESET, part.text)
                print(DEBUG + f"DEBUG: Function to call: {RESET}{function_call.name}")
                print(DEBUG + f"DEBUG: Arguments: {RESET}{function_call.args}")
                results = await execute_tool(ctx, name, args)

                messages.append({"role": "model", "parts": [part]})
                messages.append(
                    {
                        "role": "user",
                        "parts": [
                            types.Part(
                                function_response=types.FunctionResponse(
                                    name=name, response=results
                                )
                            )
                        ],
                    }
                )
        else:
            print(
                DEBUG + "DEBUG: FOUND NO FUNCTION CALLS" + RESET,
                response.function_calls,
                part,
                response,
            )
            messages.append({"role": "model", "parts": [{"text": response.text}]})
            return response.text


class Listener(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or (
            message.author.bot or (message.author.id != message.guild.owner_id)
        ):
            return
        conf = get_config(message.guild.id)
        if (
            self.bot.user.mentioned_in(message)
            or message.channel.id == conf["ai_channel_id"]
        ):
            try:
                async with message.channel.typing():
                    await message.add_reaction("⚡")
                    ctx = await self.bot.get_context(message)
                    res = await prompt(ctx, message.content)
                    print(DEBUG + "DEBUG: Return value of Prompt" + RESET, res)
                await message.channel.send(res)

            except Exception as e:
                print(f"\033[31m EXCEPTION in Prompt: {type(e).__name__}: {e}")
                traceback.print_exc()
                await message.channel.send(str(e))


async def setup(bot):
    await bot.add_cog(Listener(bot))
