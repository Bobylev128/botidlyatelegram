import random

def generate_rounds(players, config):
    rounds = []
    current = players[:]

    for size in config:
        random.shuffle(current)
        groups = []

        for i in range(0, len(current), size):
            group = current[i:i+size]

            if len(group) == 1 and groups:
                groups[-1].append(group[0])
            else:
                groups.append(group)

        rounds.append(groups)
        current = ["TBD"] * len(groups)

    return rounds


def get_winners(group, r, g, count_votes):
    scores = [(u, sum(count_votes(u, r, g).values())) for u in group]
    scores.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in scores]