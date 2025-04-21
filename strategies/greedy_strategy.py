from collections import Counter

def greedy_strategy(dice, scorecard, simulator):
    # Make up to two more rolls
    for _ in range(2):
        # Try to build the highest scoring hand
        counts = Counter(dice)
        most_common = counts.most_common(1)[0][0]
        
        # Keep the most common dice, reroll others
        reroll_positions = [i for i, d in enumerate(simulator.hand.dice) if d != most_common]
        simulator.hand.reroll(reroll_positions)
        dice = simulator.hand.dice
    
    # Score in the category that gives the highest points
    available_categories = [cat for cat in scorecard if scorecard[cat] is None]
    best_score = -1
    best_category = None
    
    for category in available_categories:
        score_method = getattr(simulator.scorer, f"score_{category}")
        score = score_method(dice)
        if score > best_score:
            best_score = score
            best_category = category
    
    return best_category, simulator.hand.dice
