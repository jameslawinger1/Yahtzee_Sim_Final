import os
import random
import pandas as pd
from strategies import dice_driven, upper_focus, yahtzee_focus, hybrid

NUM_SIMULATIONS = 10000


def simulate(strategy_func):
    results = []
    for _ in range(NUM_SIMULATIONS):
        score = strategy_func()
        results.append(score)
    return results

if __name__ == "__main__":
    print("🔁 Starting simulation...")

    results = {}

    print("🎲 Simulating Dice-Driven Strategy...")
    results['Dice-Driven'] = simulate(dice_driven.play_game)

    print("📈 Simulating Upper-Focus Strategy...")
    results['Upper-Focus'] = simulate(upper_focus.play_game)

    print("💥 Simulating Yahtzee-Focus Strategy...")
    results['Yahtzee-Focus'] = simulate(yahtzee_focus.play_game)

    print("🧠 Simulating Hybrid Strategy...")
    results['Hybrid'] = simulate(hybrid.play_game)

    df = pd.DataFrame(results)
    print("✅ DataFrame created:")
    print(df.head())

    # Ensure the folder exists
    os.makedirs("results", exist_ok=True)
    
    output_path = "results/scores_by_strategy.csv"
    df.to_csv(output_path, index=False)

    print(f"✅ Simulation complete. Results saved to: {output_path}")