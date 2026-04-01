def format_round(round_n, group, time_left):
    text = f"💬 БАТЛ ЮЗОВ\n🏁 Раунд {round_n+1}\n\n"

    for u in group:
        text += f"{u}\n"

    text += f"\n⏳ До конца: {time_left}"
    text += "\n\n👇 ГОЛОСУЙ НИЖЕ 👇"

    return text