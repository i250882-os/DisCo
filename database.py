import sqlite3
from logs import logger


def init_database():
    conn = sqlite3.connect("disco.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS server_configs (
            guild_id TEXT PRIMARY KEY,
            log_channel_id TEXT,
            initialized BOOLEAN,
            ai_channel_id TEXT
        )
    """)
    conn.commit()
    cursor.close()


def check_initialized(guild_id) -> bool:
    conn = sqlite3.connect("disco.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM server_configs WHERE guild_id = ? LIMIT 1", (str(guild_id),)
    )
    exists = cursor.fetchone() is not None
    cursor.close()
    return exists


def initialize_guild(guild_id, log_channel_id, ai_channel_id):
    exists = check_initialized(guild_id)
    logger.debug(f"DEBUG: Init Func {guild_id} {log_channel_id} {ai_channel_id}")
    msg = f"""
- Mention the bot or just start typing prompts in <#{ai_channel_id}>
- See Action and Error Logs in <#{log_channel_id}>
    
Note: Only server owner can prompt the bot.
    """
    if exists:
        return {"message": "Server Already Initialized!!\n" + msg}
    conn = sqlite3.connect("disco.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO server_configs (guild_id, log_channel_id, ai_channel_id, initialized) VALUES (?, ?, ?, ?)",
        (str(guild_id), str(log_channel_id), str(ai_channel_id), True),
    )
    conn.commit()
    cursor.close()
    return {"message": "Server Initialized!!\n" + msg}


def get_config(guild_id):
    exists = check_initialized(guild_id)
    if not exists:
        return {"initialized": False, "log_channel_id": None, "ai_channel_id": None}
    else:
        conn = sqlite3.connect("disco.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM server_configs WHERE guild_id = ?", (str(guild_id),))
        row = cursor.fetchone()
        print(row)
        cursor.close()
        return {
            "log_channel_id": int(row["log_channel_id"]),
            "ai_channel_id": int(row["ai_channel_id"]),
        }
