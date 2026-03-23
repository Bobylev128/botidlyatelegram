import asyncio
from db import count_votes
from battle_data import battle_data
from handlers.admin import send_round
from config import MAIN_CHANNEL_ID


async def process_round(bot):
    round_n = battle_data["current_round"]
    rounds = battle_data["rounds"]
    winners = []

    for group_n, group in enumerate(rounds[round_n]):
        best_user = None
        best_votes = -1
        for user in group:
            votes = count_votes(user, round_n, group_n)
            if votes > best_votes:
                best_votes = votes
                best_user = user
        winners.append(best_user)

    return winners


async def next_round(bot):
    current = battle_data["current_round"]
    winners = await process_round(bot)

    # сообщение победителей
    text = "🏆 Победители раунда:\n" + "\n".join(winners)
    await bot.send_message(MAIN_CHANNEL_ID, text)

    # удаление старых сообщений
    battle_data["current_round"] += 1

    if battle_data["current_round"] >= len(battle_data["rounds"]):
        await finish_battle(bot, winners)
    else:
        battle_data["rounds"][battle_data["current_round"]] = [winners[i:i+4] for i in range(0, len(winners), 4)]
        await send_round(bot, battle_data["current_round"])


async def finish_battle(bot, winners):
    config = battle_data["config"]
    prizes = config["prizes"]

    medals = ["🥇", "🥈", "🥉", "🏆"]
    text = "💬 <b>БАТЛ ЮЗОВ ОКОНЧЕН!</b>\n\n🏆 Победители:\n\n"
    for i, user in enumerate(winners):
        if i >= len(prizes):
            break
        text += f"{medals[i]} {i+1} Место:\n{user}\nПриз: {prizes[i]}⭐\n\n"
    await bot.send_message(MAIN_CHANNEL_ID, text, parse_mode="HTML")
    battle_data.clear()