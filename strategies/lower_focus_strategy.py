import random
from collections import Counter
from scoreboard import YahtzeeScorer # Assuming YahtzeeScorer is accessible
from dice_rolling import YahtzeeHand # May need hand methods

def lower_focus_strategy(dice, scorecard, simulator):
    """
    A Yahtzee strategy that prioritizes scoring in the lower section categories.
    """
    scorer = YahtzeeScorer()
    available_categories = [cat for cat, score in scorecard.items() if score is None]
    lower_categories = [
        'three_of_a_kind', 'four_of_a_kind', 'full_house',
        'small_straight', 'large_straight', 'yahtzee', 'chance'
    ]
    available_lower = [cat for cat in available_categories if cat in lower_categories]

    current_dice = list(dice)
    
    # --- Rerolling Logic ---
    # This is more complex than upper focus. We need to evaluate potential for various patterns.
    # Let's try a simplified approach: keep dice that form the best partial pattern for an available lower category.
    
    for roll_num in range(2): # Perform up to two rerolls
        counts = Counter(current_dice)
        sorted_dice = sorted(current_dice)
        unique_dice = sorted(list(set(current_dice)))
        
        keep_indices = []
        best_pattern_potential = -1 # Lower is better (0 = Yahtzee, 1 = LS, etc.)
        
        # Check potential for available lower categories (simplified priority)
        
        # 1. Yahtzee potential?
        if 'yahtzee' in available_lower:
            for num, count in counts.items():
                if count >= 3: # Keep 3 or more of the same dice for Yahtzee potential
                    potential_indices = [i for i, die in enumerate(current_dice) if die == num]
                    if len(potential_indices) > len(keep_indices): # Prioritize keeping more dice
                         keep_indices = potential_indices
                         best_pattern_potential = 0


        # 2. Large Straight potential?
        if 'large_straight' in available_lower and best_pattern_potential > 1:
             # Check for sequences of 4 or 5
             for i in range(len(unique_dice) - 3):
                 # Check for 1,2,3,4 / 2,3,4,5 / 3,4,5,6
                 is_straight_4 = all(unique_dice[i+j] == unique_dice[i]+j for j in range(4))
                 if is_straight_4:
                     # Keep all dice forming the longest straight subsequence
                     current_straight_dice = unique_dice[i:i+4]
                     potential_indices = [idx for idx, die in enumerate(current_dice) if die in current_straight_dice]
                     # Simple keep: just keep the unique ones found for now
                     potential_indices = [idx for idx, die in enumerate(sorted_dice) if die in current_straight_dice] 
                     # This logic needs refinement to handle duplicates correctly when keeping for straights.
                     # Let's keep the first occurrence of each needed die.
                     temp_indices = []
                     needed = list(current_straight_dice)
                     for idx, die in enumerate(current_dice):
                         if die in needed:
                             temp_indices.append(idx)
                             needed.remove(die) # Remove one instance
                     
                     if len(temp_indices) >= 4 and len(temp_indices) > len(keep_indices): # Keep if it's a potential LS (4+)
                         keep_indices = temp_indices
                         best_pattern_potential = 1
                     break # Found a potential straight

        # 3. Small Straight potential? (Check if LS wasn't better)
        if 'small_straight' in available_lower and best_pattern_potential > 2:
             # Check for sequences of 3 within the unique dice to form a base
             for i in range(len(unique_dice) - 2):
                 is_straight_3 = all(unique_dice[i+j] == unique_dice[i]+j for j in range(3))
                 if is_straight_3:
                     current_straight_dice = unique_dice[i:i+3]
                     # Keep first occurrence of each needed die
                     temp_indices = []
                     needed = list(current_straight_dice)
                     for idx, die in enumerate(current_dice):
                         if die in needed:
                             temp_indices.append(idx)
                             needed.remove(die)
                             
                     if len(temp_indices) >= 3 and len(temp_indices) > len(keep_indices): # Keep if potential SS (3+)
                         keep_indices = temp_indices
                         best_pattern_potential = 2
                     # Don't break, maybe a better SS sequence exists

        # 4. Full House potential? (Keep pairs and triples)
        if 'full_house' in available_lower and best_pattern_potential > 3:
            pairs = [num for num, count in counts.items() if count >= 2]
            triples = [num for num, count in counts.items() if count >= 3]
            if triples and pairs: # Potential FH
                 triple_val = triples[0] # Assume only one triple matters for now
                 pair_val = [p for p in pairs if p != triple_val]
                 if pair_val:
                     pair_val = pair_val[0]
                     potential_indices = [i for i, die in enumerate(current_dice) if die == triple_val or die == pair_val]
                     if len(potential_indices) == 5: # Already have FH
                          keep_indices = potential_indices
                          best_pattern_potential = 3
                     elif len(potential_indices) > len(keep_indices): # Keep partial FH
                          keep_indices = potential_indices
                          best_pattern_potential = 3


        # 5. Four of a Kind potential?
        if 'four_of_a_kind' in available_lower and best_pattern_potential > 4:
             for num, count in counts.items():
                 if count >= 3: # Keep 3+ for 4oak potential
                     potential_indices = [i for i, die in enumerate(current_dice) if die == num]
                     if len(potential_indices) > len(keep_indices):
                         keep_indices = potential_indices
                         best_pattern_potential = 4

        # 6. Three of a Kind potential?
        if 'three_of_a_kind' in available_lower and best_pattern_potential > 5:
             for num, count in counts.items():
                 if count >= 2: # Keep 2+ for 3oak potential
                     potential_indices = [i for i, die in enumerate(current_dice) if die == num]
                     if len(potential_indices) > len(keep_indices):
                         keep_indices = potential_indices
                         best_pattern_potential = 5

        # --- Perform Reroll ---
        dice_to_reroll_count = 5 - len(keep_indices)
        
        if dice_to_reroll_count == 0: # Already keeping all dice
             break
        
        # Determine indices to reroll
        indices_to_reroll = [i for i in range(5) if i not in keep_indices]

        if dice_to_reroll_count > 0:
             # Use the correct reroll method from YahtzeeHand
             simulator.hand.reroll(indices_to_reroll)
             current_dice = list(simulator.hand.dice) # Update current_dice after reroll

        # Update hand state for next potential reroll evaluation
        counts = Counter(current_dice)
        sorted_dice = sorted(current_dice)
        unique_dice = sorted(list(set(current_dice)))


    final_dice = tuple(current_dice)

    # --- Category Selection Logic ---
    best_score = -1
    best_category = None

    # Prioritize available lower categories
    if available_lower:
        # Simple approach: iterate and find highest score in available lower
        for category in available_lower:
            score_method = getattr(scorer, f"score_{category}")
            score = score_method(final_dice)
            if score > best_score:
                best_score = score
                best_category = category
            # Special case: Prioritize Yahtzee if score is 50
            elif category == 'yahtzee' and score == 50:
                 best_score = score
                 best_category = category
                 break # Take Yahtzee immediately

    # If no suitable lower category found or scored (score <= 0), consider upper/chance
    if best_category is None or best_score <= 0:
        # Fallback: Check upper section or chance for highest score
        fallback_categories = [cat for cat in available_categories if cat not in available_lower]
        if 'chance' in available_categories: # Check chance separately? Or just include in loop
             fallback_categories.append('chance')
             
        current_best_fallback_score = -1 # Use separate variable to not overwrite potential 0 score in lower
        
        for category in fallback_categories:
             # Avoid overwriting if we already selected a lower category (even if score is 0)
             if category in scorecard and scorecard[category] is not None: continue 
             
             score_method = getattr(scorer, f"score_{category}")
             score = score_method(final_dice)
             if score > current_best_fallback_score:
                 current_best_fallback_score = score
                 # Only select this fallback category if we haven't found *any* lower category yet
                 if best_category is None: 
                     best_category = category
                     best_score = score # Update best_score as well

    # If still no category found (e.g., all scores are 0 and all categories taken?), pick first available
    if best_category is None:
        if available_categories:
             best_category = available_categories[0] # Take the first available to zero it out
        else:
             # Should not happen in a normal game
             return 'chance', final_dice # Absolute fallback

    return best_category, final_dice