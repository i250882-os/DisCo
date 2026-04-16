import discord
from logs import logger
from discord.ext.commands import Context
from database import get_config
DEBUG = "\033[33m"
RESET = "\033[0m"

# ==== Create Text ====
create_text_channel_function = {
    "name": "create_text_channel",
    "description": "Creates a text channel in the server",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the channel",
            },
            "topic": {
                "type": "string",
                "description": "The channel topic shown at the top of the channel",
            },
            "category_id": {
                "type": "string",
                "description": "ID of the category to place this channel under",
            },
            "position": {
                "type": "integer",
                "description": "Position of the channel in the channel list",
            },
            "nsfw": {
                "type": "boolean",
                "description": "Whether the channel is NSFW (age-restricted)",
            },
            "news": {
                "type": "boolean",
                "description": "Whether this is an announcement channel",
            },
            "reason": {
                "type": "string",
                "description": "Reason for creating the channel (shown in audit log)",
            },
        },
        "required": ["name"],
    },
}


async def create_text_channel(
    ctx: Context,
    name: str,
    topic: str,
    category_id: str,
    position: int,
    nsfw: bool,
    news: bool,
    reason: str,
):
    if not ctx.guild:
        return False
    kwargs = {}
    if topic:
        kwargs["topic"] = topic
    if category_id:
        kwargs["category"] = discord.Object(id=int(category_id))
    if position is not None:
        kwargs["position"] = position
    if nsfw:
        kwargs["nsfw"] = nsfw
    if news:
        kwargs["news"] = news
    if reason:
        kwargs["reason"] = reason
    channel = await ctx.guild.create_text_channel(name, **kwargs)
    if channel:
        return {"channel": "created", "name": channel.name, "id": channel.id}


# ==== Create Voice ====
create_voice_channel_function = {
    "name": "create_voice_channel",
    "description": "Creates a voice channel in the server",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the voice channel",
            },
            "category_id": {
                "type": "string",
                "description": "ID of the category to place this channel under",
            },
            "position": {
                "type": "integer",
                "description": "Position of the channel in the channel list",
            },
            "bitrate": {
                "type": "integer",
                "description": "Audio bitrate in bits per second (8000 to 96000, or up to 384000 for boosted servers)",
            },
            "user_limit": {
                "type": "integer",
                "description": "Maximum number of users allowed in the channel (0 for unlimited, max 99)",
            },
            "nsfw": {
                "type": "boolean",
                "description": "Whether the channel is NSFW (age-restricted)",
            },
            "reason": {
                "type": "string",
                "description": "Reason for creating the channel (shown in audit log)",
            },
            "rtc_region": {
                "type": "string",
                "description": "Voice region for the channel (null for automatic)",
            },
        },
        "required": ["name"],
    },
}


async def create_voice_channel(
    ctx: Context,
    name: str,
    category_id: str,
    position: int,
    bitrate: int,
    user_limit: int,
    nsfw: bool,
    reason: str,
    rtc_region: str | None = None,
):
    if not ctx.guild:
        return False
    kwargs = {}
    if category_id:
        kwargs["category"] = discord.Object(id=int(category_id))
    if position is not None:
        kwargs["position"] = position
    if bitrate is not None:
        kwargs["bitrate"] = bitrate
    if user_limit is not None:
        kwargs["user_limit"] = user_limit
    if nsfw:
        kwargs["nsfw"] = nsfw
    if reason:
        kwargs["reason"] = reason
    kwargs["rtc_region"] = rtc_region
    channel = await ctx.guild.create_voice_channel(name)
    if channel:
        return {"channel": "created", "name": channel.name, "id": channel.id}


# ==== Delete Channel ====
delete_channel_function = {
    "name": "delete_channel",
    "description": "Permanently deletes a voice or text channel from the server",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The unique ID of the channel to delete",
            },
            "reason": {
                "type": "string",
                "description": "Reason for deleting the channel (shown in audit log)",
            },
        },
        "required": ["id"],
    },
}


async def delete_channel(ctx: Context, id: str, reason: str | None = None):
    if not ctx.guild:
        return False

    channel = ctx.guild.get_channel(int(id))
    conf = get_config(ctx.guild.id).values()
    logger.debug(f"{conf} {id in conf}")
    if int(id) in conf:
        return {"channel": "not deleted", "reason": "Cant delete special AI channels"}
    if channel:
        await channel.delete(reason=reason)
        return {"channel": "deleted", "id": str(id)}
    else:
        return False


# ==== Edit Channel ====
edit_channel_function = {
    "name": "edit_channel_name",
    "description": "Edit properties of an existing channel including name, topic, category, position, and settings",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "The unique ID of the channel to edit",
            },
            "new_name": {
                "type": "string",
                "description": "New name for the channel",
            },
            "topic": {
                "type": "string",
                "description": "New topic for the channel (text channels only)",
            },
            "category_id": {
                "type": "string",
                "description": "ID of the category to move this channel to",
            },
            "position": {
                "type": "integer",
                "description": "New position of the channel in the channel list",
            },
            "nsfw": {
                "type": "boolean",
                "description": "Whether the channel should be NSFW (age-restricted)",
            },
            "news": {
                "type": "boolean",
                "description": "Whether this should be an announcement channel",
            },
            "sync_permissions": {
                "type": "boolean",
                "description": "Whether to sync permissions with the parent category",
            },
            "reason": {
                "type": "string",
                "description": "Reason for editing the channel (shown in audit log)",
            },
        },
        "required": ["id"],
    },
}


async def edit_channel(
    ctx: Context,
    id,
    new_name: str,
    topic: str,
    category_id: str,
    position: int,
    nsfw: bool,
    news: bool,
    sync_permissions: bool,
    reason: str | None = None,
):
    if not ctx.guild:
        return False
    if type(id) == str:
        id = int(id)

    channel = ctx.guild.get_channel(id)
    if channel:
        kwargs = {}
        if new_name:
            kwargs["name"] = new_name
        if topic:
            kwargs["topic"] = topic
        if category_id:
            kwargs["category"] = discord.Object(id=int(category_id))
        if position is not None:
            kwargs["position"] = position
        if nsfw:
            kwargs["nsfw"] = nsfw
        if news:
            kwargs["news"] = news
        if sync_permissions:
            kwargs["sync_permissions"] = sync_permissions
        if reason:
            kwargs["reason"] = reason

        old_name = channel.name
        await channel.edit(**kwargs)
        return {"channel": "edited", "old_name": old_name, "new_name": channel.name}


# ==== Edit Channel Permissions ====
#
# "topic": {},
# "category_id": {},
# "position": {},
# "topic": {},
# "nsfw": {},
# "news": {},
# "reason": {},
# "sync_permissions": {},
async def edit_channel_permissions(ctx: Context): ...


# ==== Get Channels List =====
get_channels_function = {
    "name": "get_channels",
    "description": "Retrieves a list of all channels in the server. Returns channel information including: id, name, position, category_name, and channel_type (text, voice, category, etc.)",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


async def get_channels(ctx: Context):
    if not ctx.guild:
        return False
    channels = [
        (
            str(channel.id),
            channel.name,
            str(channel.position),
            channel.category.name if channel.category else "uncatorized",
            str(channel.type),
        )
        for channel in ctx.guild.channels
    ]
    return channels


# === Get Server Info ===
get_server_info_function = {
    "name": "get_server_info",
    "description": "Retrieves detailed information about the server including: id, name, owner_id, member_count, channels_count, roles_count, and created_at timestamp",
    "parameters": {
        "type": "object",
        "properties": {},
    },
}


async def get_server_info(ctx: Context):
    if not ctx.guild:
        return False
    return {
        "id": str(ctx.guild.id),
        "name": ctx.guild.name,
        "owner_id": str(ctx.guild.owner_id),
        "member_count": ctx.guild.member_count,
        "channels_count": len(ctx.guild.channels),
        "roles_count": len(ctx.guild.roles),
        "created_at": str(ctx.guild.created_at),
    }


# === Create Category ===
create_category_function = {
    "name": "create_category",
    "description": "Creates a category to organize channels. Categories group text and voice channels together.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the category",
            },
            "reason": {
                "type": "string",
                "description": "Reason for creating the category (shown in audit log)",
            },
        },
        "required": ["name"],
    },
}


async def create_category(ctx: Context, name: str, reason: str | None = None):
    if not ctx.guild:
        return False
    category = await ctx.guild.create_category(name=name, reason=reason)
    if category:
        return {"category": "created", "name": category.name, "id": category.id}
    return False


channel_function_declarations = [
    create_text_channel_function,
    create_voice_channel_function,
    delete_channel_function,
    get_channels_function,
    edit_channel_function,
    create_category_function,
    get_server_info_function,
]
channel_function_map = {
    "create_text_channel": create_text_channel,
    "create_voice_channel": create_voice_channel,
    "delete_channel": delete_channel,
    "get_channels": get_channels,
    "edit_channel_name": edit_channel,
    "create_category": create_category,
    "get_server_info": get_server_info,
}
