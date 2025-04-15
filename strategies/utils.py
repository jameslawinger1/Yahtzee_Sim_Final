import random
from collections import Counter

def roll_dice(num):
    return [random.randint(1, 6) for _ in range(num)]

def reroll(dice, keep_indices):
    return [dice[i] if i in keep_indices else random.randint(1, 6) for i in range(5)]

def score_upper(dice):
    return sum(dice)

def is_yahtzee(dice):
    return len(set(dice)) == 1

def score_yahtzee(dice):
    return 50 if is_yahtzee(dice) else 0
