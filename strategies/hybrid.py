from .utils import roll_dice, reroll
from collections import Counter

def upper_focus_turn(target):
    dice = roll_dice(5)
    for _ in range(2):
        keep_indices = [i for i, val in enumerate(dice) if val == target]
        dice = reroll(dice, keep_indices)
    return sum([d for d in dice if d == target])

def dice_driven_turn():
    dice = roll_dice(5)

    for _ in range(2):
        counts = Counter(dice)
        most_common = counts.most_common(1)[0][0]
        keep_indices = [i for i, die in enumerate(dice) if die == most_common]
        dice = reroll(dice, keep_indices)

    counts = Counter(dice)
    most_common_count = counts.most_common(1)[0][1]

    # Scoring rules
    if most_common_count == 5:
        return 50  # Yahtzee
    elif most_common_count == 4 or most_common_count == 3:
        return sum(dice)  # 3 or 4 of a kind
    else:
        return sum(dice) // 2  # fallback: partial score

def play_game():
    total_score = 0
    upper_score = 0

    # First 6 turns: target 1s through 6s
    for i in range(6):
        score = upper_focus_turn(i + 1)
        upper_score += score
        total_score += score

    # Check for bonus
    if upper_score >= 63:
        total_score += 35

    # Final 7 turns: optimized dice play
    for _ in range(7):
        total_score += dice_driven_turn()

    return total_score
