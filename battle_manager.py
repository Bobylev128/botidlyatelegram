import asyncio
from keyboards.inline import vote_kb
from utils.timer import loop
import aiosqlite

class Battle:

    def __init__(self):
        self.players = []
        self.rounds = []
        self.prizes = []

    def split(self, players, size):
        return [players[i:i+size] for i in range(0, len(players), size)]

    async def run(self, bot, chat_id):

        current = self.players

        for r_index, size in enumerate(self.rounds):

            groups = self.split(current, size)
            winners = []

            for i, group in enumerate(groups):

                gid = f"{r_index}_{i}"

                msg = await bot.send_message(
                    chat_id,
                    "Раунд",
                    reply_markup=vote_kb(gid, group)
                )

                asyncio.create_task(loop(bot, chat_id, msg.message_id, group, gid))

                await asyncio.sleep(3600)

                async with aiosqlite.connect("battle.db") as db:
                    cur = await db.execute(
                        "SELECT target, COUNT(*) FROM votes WHERE group_id=? GROUP BY target",
                        (gid,))
                    votes = dict(await cur.fetchall())

                winner = max(group, key=lambda u: votes.get(u,0))
                winners.append(winner)

            current = winners

        return current