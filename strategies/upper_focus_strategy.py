import random
from collections import Counter
from scoreboard import YahtzeeScorer # Assuming YahtzeeScorer is accessible

def upper_focus_strategy(dice, scorecard, simulator):
    """
    A Yahtzee strategy that prioritizes scoring in the upper section categories
    to achieve the bonus.
    """
    scorer = YahtzeeScorer()
    available_categories = [cat for cat, score in scorecard.items() if score is None]
    upper_categories = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes']
    available_upper = [cat for cat in available_categories if cat in upper_categories]

    current_dice = list(dice)
    
    # --- Rerolling Logic ---
    for roll_num in range(2): # Perform up to two rerolls
        counts = Counter(current_dice)
        keep_indices = []

        # Determine best upper category target currently available
        best_target_num = 0
        if available_upper:
            # Prioritize higher numbers first if available
            for num in range(6, 0, -1):
                 num_str = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'][num-1]
                 if num_str in available_upper:
                     best_target_num = num
                     break
        
        # Keep dice matching the best target number
        if best_target_num > 0:
            for i, die in enumerate(current_dice):
                if die == best_target_num:
                    keep_indices.append(i)
        
        # If no upper target or no dice match, maybe keep high dice for other categories?
        # For simplicity now, if no upper target, we won't specifically keep anything, leading to a full reroll.
        # Or, if we kept some dice, reroll the rest.

        dice_to_reroll_count = 5 - len(keep_indices)
        
        if dice_to_reroll_count == 0: # Already keeping all dice
             break
        
        # Determine indices to reroll
        indices_to_reroll = [i for i in range(5) if i not in keep_indices]

        if dice_to_reroll_count > 0:
             # Use the correct reroll method from YahtzeeHand
             simulator.hand.reroll(indices_to_reroll)
             current_dice = list(simulator.hand.dice) # Update current_dice after reroll

        if not available_upper and roll_num == 0: # If no upper categories left on first reroll, maybe stop early?
             pass # Continue rerolling for potentially good lower scores

    final_dice = tuple(current_dice)

    # --- Category Selection Logic ---
    best_score = -1
    best_category = None

    # Prioritize available upper categories
    if available_upper:
        for category in available_upper:
            score_method = getattr(scorer, f"score_{category}")
            score = score_method(final_dice)
            # Try to score *something* in the target category if possible
            target_num = ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'].index(category) + 1
            if counts.get(target_num, 0) > 0 and score > best_score: # Ensure we actually have dice for the category
                 # Heuristic: Prefer filling the category even if score is low, if it's an upper one?
                 # Let's stick to highest score for now.
                 best_score = score
                 best_category = category

    # If no suitable upper category found or scored, consider all available categories
    if best_category is None:
        best_score = -1 # Reset best score search
        for category in available_categories:
            score_method = getattr(scorer, f"score_{category}")
            score = score_method(final_dice)
            if score > best_score:
                best_score = score
                best_category = category

    # If still no category found (e.g., all scores are 0), pick a random available one
    if best_category is None:
        if available_categories:
             best_category = random.choice(available_categories)
        else:
             # This case shouldn't happen in a normal 13-round game
             return 'chance', final_dice # Fallback

    return best_category, final_dice