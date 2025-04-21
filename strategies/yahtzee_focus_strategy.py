import random
from collections import Counter
from scoreboard import YahtzeeScorer # Assuming YahtzeeScorer is accessible

def yahtzee_focus_strategy(dice, scorecard, simulator):
    """
    A Yahtzee strategy that aggressively tries to roll a Yahtzee.
    """
    scorer = YahtzeeScorer()
    available_categories = [cat for cat, score in scorecard.items() if score is None]
    
    current_dice = list(dice)

    # --- Rerolling Logic ---
    for roll_num in range(2): # Perform up to two rerolls
        counts = Counter(current_dice)
        
        # Find the number that appears most often (must be at least 2 times)
        most_common_num = -1
        max_count = 1 
        for num, count in counts.items():
            if count > max_count:
                max_count = count
                most_common_num = num
            # Tie-breaking: prefer higher numbers if counts are equal? Let's keep it simple for now.
            
        keep_indices = []
        if max_count >= 2: # If we have at least a pair, keep those dice
            keep_indices = [i for i, die in enumerate(current_dice) if die == most_common_num]
        # else: If no pair or better, keep_indices remains empty, reroll all.

        # --- Perform Reroll ---
        dice_to_reroll_count = 5 - len(keep_indices)
        
        if dice_to_reroll_count == 0: # Already keeping all dice (likely have a Yahtzee or decided to keep 5)
             break 
        
        # Determine indices to reroll
        indices_to_reroll = [i for i in range(5) if i not in keep_indices]

        if dice_to_reroll_count > 0:
             # Use the correct reroll method from YahtzeeHand
             simulator.hand.reroll(indices_to_reroll)
             current_dice = list(simulator.hand.dice) # Update current_dice after reroll

    final_dice = tuple(current_dice)
    final_counts = Counter(final_dice)

    # --- Category Selection Logic ---
    best_score = -1
    best_category = None
    is_yahtzee = 5 in final_counts.values()

    # 1. Prioritize scoring Yahtzee if available and achieved
    if 'yahtzee' in available_categories and is_yahtzee:
        best_category = 'yahtzee'
        best_score = scorer.score_yahtzee(final_dice) # Should be 50
    
    # 2. If Yahtzee category used OR not achieved, find the best score elsewhere
    else:
        # If we have a Yahtzee but the category is used, check for Yahtzee Bonus rules (not implemented here)
        # For now, just find the highest score in any available category.
        
        best_score = -1 # Reset search
        for category in available_categories:
            # Skip Yahtzee category if we didn't roll one this turn
            if category == 'yahtzee' and not is_yahtzee:
                continue

            score_method = getattr(scorer, f"score_{category}")
            score = score_method(final_dice)
            
            # Simple highest score selection among remaining options
            if score > best_score:
                best_score = score
                best_category = category
            # If scores are equal, maybe prioritize lower section? Or upper? Keep simple for now.

    # 3. If no category yields a score > 0 (or all taken), pick a category to zero out
    if best_category is None:
         # Try to zero out a less valuable category first.
         # Simplification: Zero out an upper category if possible, otherwise lower.
         upper_categories = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
         available_upper = [cat for cat in available_categories if cat in upper_categories]
         available_lower = [cat for cat in available_categories if cat not in upper_categories and cat != 'yahtzee'] # Exclude yahtzee if not scored

         if available_upper:
             # Zero out the lowest available upper category first? e.g., 'ones'
             best_category = min(available_upper, key=lambda cat: upper_categories.index(cat))
         elif available_lower:
              # Zero out 'chance' or 'three_of_a_kind' if available?
              if 'chance' in available_lower: best_category = 'chance'
              elif 'three_of_a_kind' in available_lower: best_category = 'three_of_a_kind'
              else: best_category = random.choice(available_lower) # Random lower if others taken
         elif 'yahtzee' in available_categories: # Only remaining option is Yahtzee, score 0
              best_category = 'yahtzee'
         else:
              # Should not happen in a normal game
              return 'chance', final_dice # Absolute fallback

    return best_category, final_dice