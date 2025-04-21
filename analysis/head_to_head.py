import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load all strategy score files and simulate head-to-head matchups.
# We'll compare how often each strategy outscores the others.

results_dir = "results"
plots_dir = "plots"
os.makedirs(plots_dir, exist_ok=True)

files = [f for f in os.listdir(results_dir) if f.endswith("_scores.csv")]
strategies = [f.replace("_scores.csv", "") for f in files]
data = {s: pd.read_csv(os.path.join(results_dir, f"{s}_scores.csv"))["score"].values for s in strategies}

n_matches = 20000
win_matrix = pd.DataFrame(0.0, index=strategies, columns=strategies)

for s1 in strategies:
    for s2 in strategies:
        s1_scores = np.random.choice(data[s1], size=n_matches)
        s2_scores = np.random.choice(data[s2], size=n_matches)
        win_rate = np.mean(s1_scores > s2_scores)
        win_matrix.loc[s1, s2] = round(win_rate, 3)

# Save table as CSV
win_matrix.to_csv(os.path.join(results_dir, "head_to_head_winrates.csv"))
print("\nHead-to-head win rates (% of times row strategy beats column):")
print(win_matrix)

# Plot heatmap
plt.figure(figsize=(8, 6))
im = plt.imshow(win_matrix.values, cmap="coolwarm", vmin=0, vmax=1)
plt.colorbar(im, label="Win Probability")
plt.xticks(ticks=np.arange(len(strategies)), labels=strategies, rotation=45, ha="right")
plt.yticks(ticks=np.arange(len(strategies)), labels=strategies)
plt.title("Who Beats Who? (Head-to-Head Win %)")
for i in range(len(strategies)):
    for j in range(len(strategies)):
        plt.text(j, i, f"{win_matrix.iloc[i, j]:.2f}", ha="center", va="center", color="black")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "head_to_head_heatmap.png"))
plt.close()

print("✓ Head-to-head heatmap saved to 'plots/'.")