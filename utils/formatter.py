def final_text(winners, prizes):
    medals = ["🥇","🥈","🥉","🏆"]
    text = "🏆 БАТЛ ОКОНЧЕН\n\n"

    for i, u in enumerate(winners):
        text += f"{medals[i]} {u}\nПриз: {prizes[i]}⭐\n\n"

    return text