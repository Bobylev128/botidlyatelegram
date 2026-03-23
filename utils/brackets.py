def generate_brackets(users, group_size=4):
    groups = [users[i:i+group_size] for i in range(0, len(users), group_size)]
    return groups