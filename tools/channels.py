import discord
from discord.ext.commands import Context

async def create(ctx: Context):
    if not ctx.guild:
        return

    await ctx.guild.create_text_channel("Test")
