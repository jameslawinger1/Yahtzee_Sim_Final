from .utils import roll_dice, reroll, score_upper, score_yahtzee
from collections import Counter

def play_game():
    total_score = 0
    used_categories = set()

    for turn in range(13):
        dice = roll_dice(5)

        # Keep the most common value for rerolls
        for _ in range(2):
            counts = Counter(dice)
            most_common = counts.most_common(1)[0][0]
            keep_indices = [i for i, die in enumerate(dice) if die == most_common]
            dice = reroll(dice, keep_indices)

        counts = Counter(dice)
        most_common_count = counts.most_common(1)[0][1]

        # Choose scoring category: Yahtzee > Four of a Kind > Three > Upper Section
        if most_common_count == 5 and 'Yahtzee' not in used_categories:
            total_score += 50
            used_categories.add('Yahtzee')
        elif most_common_count == 4 and 'FourKind' not in used_categories:
            total_score += sum(dice)
            used_categories.add('FourKind')
        elif most_common_count == 3 and 'ThreeKind' not in used_categories:
            total_score += sum(dice)
            used_categories.add('ThreeKind')
        else:
            # Upper section scoring fallback
            best_num = counts.most_common(1)[0][0]
            score = best_num * counts[best_num]
            total_score += score
            used_categories.add(f"Upper-{best_num}")

    return total_score
