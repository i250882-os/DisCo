import sqlite3

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
    cursor.execute("SELECT 1 FROM server_configs WHERE guild_id = ? LIMIT 1", (guild_id,))
    exists = cursor.fetchone() is not None
    print(exists)
    cursor.close()
    return exists 

def initialize_guild(guild_id, log_channel_id, ai_channel):
    exists = check_initialized(guild_id)
    if exists:
        return {"message": "Server Already Initialized!!"}
    conn = sqlite3.connect("disco.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (guild_id, log_channel_id, ai_channel_id, initialized) VALUES (?, ?, ?, ?)", (guild_id, log_channel_id, ai_channel, True))
    cursor.close()
    return {"message": "Server Initialized!!"}

def get_config(guild_id):
    exists = check_initialized(guild_id)
    if not exists:
        return {
            "initialized": False,
            "log_channel_id": None,
            "ai_channel_id": None
        }
    else:
        conn = sqlite3.connect("disco.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM server_configs WHERE guild_id = ?", (guild_id,))
        row = cursor.fetchone()
        cursor.close()
        return {
            "log_channel_id": row["log_channel_id"],
            "ai_channel_id": row["ai_channel_id"] 
        }
