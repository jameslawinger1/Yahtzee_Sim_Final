from .utils import roll_dice, reroll
from collections import Counter

def play_game():
    total_score = 0
    upper_score = 0
    used_numbers = set()

    for turn in range(6):  # Focus only on 1s to 6s
        target = turn + 1
        dice = roll_dice(5)

        for _ in range(2):
            keep_indices = [i for i, val in enumerate(dice) if val == target]
            dice = reroll(dice, keep_indices)

        score = sum([d for d in dice if d == target])
        upper_score += score
        used_numbers.add(target)

    # Bonus if upper section >= 63
    if upper_score >= 63:
        upper_score += 35

    total_score += upper_score

    # Fill rest of the 13 turns with filler rolls
    for _ in range(7):
        total_score += sum(roll_dice(5)) // 2  # dummy logic

    return total_score
