def create_vote_link(bot_username, round_n, group_n):
    return f"https://t.me/{bot_username}?start=vote_{round_n}_{group_n}"


def create_join_link(bot_username):
    return f"https://t.me/{bot_username}?start=join"