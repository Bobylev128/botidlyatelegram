import asyncio
import aiosqlite

async def get_votes(group_id):
    async with aiosqlite.connect("battle.db") as db:
        cur = await db.execute("SELECT target, COUNT(*) FROM votes WHERE group_id=? GROUP BY target", (group_id,))
        return dict(await cur.fetchall())

async def loop(bot, chat_id, msg_id, group, gid):
    while True:
        votes = await get_votes(gid)

        text = "🔥 БАТЛ\n\n"
        for u in group:
            text += f"{u} — {votes.get(u,0)}\n"

        try:
            await bot.edit_message_text(text, chat_id, msg_id)
        except:
            pass

        await asyncio.sleep(10)