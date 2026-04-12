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
    channel = await ctx.guild.create_text_channel(name)
    if channel:
        return {"channel": "created", "name": channel.name, "id": channel.id}
    

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
    channel = await ctx.guild.create_voice_channel(name)
    if channel:
        return {"channel": "created", "name": channel.name, "id": channel.id}


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
    if type(id) == str:
        id = int(id)
    channel = ctx.guild.get_channel(id)
    if channel:
        await channel.delete()
        return {"channel": "deleted", "id": str(id)}
    else:
        return False

# ==== Edit Channel Name ====
edit_channel_name_function = {
    "name": "edit_channel_name",
    "description": "Edit name of an exisitng channel", 
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "unique ID of the channel"
            },
            "new_name": {
                "type": "string",
                "description": "New Name of the channel"
            },
        },
    },
}
async def edit_channel_name(ctx: Context, id, new_name: str):
    if not ctx.guild:
        return False
    if type(id) == str:
        id = int(id)

    channel = ctx.guild.get_channel(id)
    if channel:
        old_name = channel.name
        await channel.edit(name=new_name)
        return {"channel": "renamed", "old_name": old_name, "new_name": channel.name}

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
    channels = [(str(channel.id), channel.name) for channel in ctx.guild.channels]
    return channels




channel_function_declarations = [
    create_text_channel_function,
    create_voice_channel_function,
    delete_channel_function,
    get_channels_function,
    edit_channel_name_function
]
channel_function_map = {
    "create_text_channel": create_text_channel,
    "create_voice_channel": create_voice_channel,
    "delete_channel": delete_channel,
    "get_channels": get_channels,
    "edit_channel_name": edit_channel_name,
}
