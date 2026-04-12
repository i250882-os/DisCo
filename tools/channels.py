import discord
from discord.ext.commands import Context

# ==== Create Text ====
create_text_channel_function = {
    "name": "create_text_channel",
    "description": "Creates a text channel",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the channel",
            },
        },
        "required": ["name"],
    },
}
async def create_text_channel(ctx: Context, name: str):
    if not ctx.guild:
        return False
    await ctx.guild.create_text_channel(name)

# ==== Create Voice ====
create_voice_channel_function = {
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
}
async def create_voice_channel(ctx: Context, name: str):
    if not ctx.guild:
        return False
    await ctx.guild.create_voice_channel(name)

# ==== Delete Channel ====
delete_channel_function = {
    "name": "delete_channel",
    "description": "Deletes voice or text channel", 
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "ID of the channel"
            },
        },
    },
}
async def delete_channel(ctx: Context, id):
    if not ctx.guild:
        return False
    channel = ctx.guild.get_channel(id)
    if channel:
        await channel.delete()
        return True
    else:
        return False

# ==== Edit Channel Name ====
async def edit_name(ctx: Context, id: int, name: str):
    if not ctx.guild:
        return False
    channel = ctx.guild.get_channel(id)
    if channel:
        await channel.edit(name=name)

# ==== Edit Channel Permissions ====
async def edit_permissions(ctx: Context):
    ...

# ==== Get Channels List =====
get_channels_function = {
    "name": "get_channels",
    "description": "Gives list of all the channels in a server with their IDs and Name", 
}
async def get_channels(ctx: Context):
    if not ctx.guild:
        return False
    channels = [(channel.id, channel.name) for channel in ctx.guild.channels]
    return channels




channel_function_declarations = [
    create_text_channel_function,
    create_voice_channel_function,
    delete_channel_function,
    get_channels_function
]
