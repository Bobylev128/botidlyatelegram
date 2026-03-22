import aiosqlite

DB = "battle.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:

        await db.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER, username TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS participants(user_id INTEGER, username TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS blacklist(user_id INTEGER)")
        await db.execute("CREATE TABLE IF NOT EXISTS votes(voter_id INTEGER, group_id TEXT, target TEXT, type TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS settings(key TEXT, value TEXT)")

        await db.commit()