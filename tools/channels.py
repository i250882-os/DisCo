import discord
from discord.ext.commands import Context

DEBUG = "\033[33m"
RESET = "\033[0m"

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

# ==== Edit Channel Position ====
edit_channel_position_function = {
    "name": "edit_channel_position",
    "description": "Edit position of the channel",
    "parameters": {
        "type": "object",
        "properties": {
            "channel_id": {
                "type": "string",
                "description": "unique ID of the channel to be moved"
            },
            "position": {
                "type": "string",
                "description": "The position in the channel list. This is a number that starts at 0. e.g. the top channel is position 0."
            },
            "category_id": {
                "type": "string",
                "description": "ID of the category to move to"
            },
        },
        "required": ["channel_id"],
    },
}
async def edit_channel_position(ctx: Context, channel_id= "", position= "", category_id= ""):
    if not ctx.guild:
        return False

    channel_id = int(channel_id) if channel_id else -1
    position = int(position) if position else -1
    category_id = int(category_id) if category_id else -1

    channel = await ctx.bot.fetch_channel(channel_id)
    category = await ctx.bot.fetch_channel(category_id)
    print(DEBUG+"FUNC: VALUES", type(channel), type(category), channel_id, category_id, position)
    if not channel or (position == -1) and (not isinstance(category, discord.CategoryChannel)): 
        return False 
    if isinstance(category, discord.CategoryChannel): 
        await channel.edit(category=category)
        print("LOG: CHANNEL MOVED TO CATEGORY")
    if position != -1:
        await channel.edit(position=position)
        print("LOG: CHANNEL MOVED TO POSITION")
    
    channel = await ctx.bot.fetch_channel(channel_id)
    return {"position": channel.position, "category": channel.category.id}

# ==== Edit Channel Permissions ====
async def edit_permissions(ctx: Context):
    ...

# ==== Get Channels List =====
get_channels_function = {
    "name": "get_channels",
    "description": "Gives list of all the channels in a server, The returned data includes the following information about a channel (id, name, position, category_name, channel_type)", 
}
async def get_channels(ctx: Context):
    if not ctx.guild:
        return False
    channels = [(str(channel.id), channel.name, str(channel.position), channel.category.name if channel.category else "uncatorized", str(channel.type)) for channel in ctx.guild.channels]
    return channels

# === Create Category ===
create_category_function = {
    "name": "create_category",
    "description": "creats a category of channels",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of teh category"
            },
        },
    },
}
async def create_category(ctx: Context, name):
    if not ctx.guild:
        return False
    category = await ctx.guild.create_category(name=name)
    if category:
        return {"category": "created", "name": category.name}
    return False



channel_function_declarations = [
    create_text_channel_function,
    create_voice_channel_function,
    delete_channel_function,
    get_channels_function,
    edit_channel_name_function,
    create_category_function,
    edit_channel_position_function,
]
channel_function_map = {
    "create_text_channel": create_text_channel,
    "create_voice_channel": create_voice_channel,
    "delete_channel": delete_channel,
    "get_channels": get_channels,
    "edit_channel_name": edit_channel_name,
    "create_category": create_category,
    "edit_channel_position": edit_channel_position
}
