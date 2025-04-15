from .utils import roll_dice, reroll, is_yahtzee

def play_game():
    total_score = 0
    yahtzee_bonus = 0

    for _ in range(13):
        dice = roll_dice(5)

        for _ in range(2):
            counts = {}
            for val in range(1, 7):
                counts[val] = dice.count(val)
            target = max(counts, key=counts.get)
            keep_indices = [i for i, die in enumerate(dice) if die == target]
            dice = reroll(dice, keep_indices)

        if is_yahtzee(dice):
            if total_score == 0:
                total_score += 50  # First Yahtzee
            else:
                yahtzee_bonus += 100  # Subsequent Yahtzees

        total_score += sum(dice) // 3  # Filler logic for other categories

    return total_score + yahtzee_bonus
