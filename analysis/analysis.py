import os
import glob
import math
import pandas as pd
import matplotlib.pyplot as plt

# This script loads all *_scores.csv files in the results directory,
# calculates summary stats for each strategy, and creates basic plots.

results_dir = "results"
plots_dir = "plots"
os.makedirs(plots_dir, exist_ok=True)

# Step 1: Load all score CSVs
score_files = glob.glob(os.path.join(results_dir, "*_scores.csv"))
scores = {}

for file in score_files:
    name = os.path.basename(file).replace("_scores.csv", "")
    df = pd.read_csv(file)
    scores[name] = df["score"]

# Step 2: Compute stats for each strategy
summary = []
for name, data in scores.items():
    mean = round(data.mean(), 2)
    median = data.median()
    std = round(data.std(), 2)
    ci = round(1.96 * data.std() / math.sqrt(len(data)), 2)
    summary.append({
        "Strategy": name,
        "Mean": mean,
        "Median": median,
        "Std Dev": std,
        "Min": data.min(),
        "Max": data.max(),
        "95% CI": ci
    })
summary_df = pd.DataFrame(summary).sort_values("Mean", ascending=False)
summary_df.to_csv(os.path.join(results_dir, "summary_stats.csv"), index=False)
print(summary_df.to_string(index=False))

# Step 3: Plot score distributions
for name, data in scores.items():
    plt.figure()
    plt.hist(data, bins=30)
    plt.title(f"{name} – Score Distribution")
    plt.xlabel("Total Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"{name}_histogram.png"))
    plt.close()

# Step 4: Boxplot comparing all strategies
plt.figure()
plt.boxplot(scores.values(), labels=scores.keys())
plt.title("Strategy Comparison – Boxplot")
plt.ylabel("Total Score")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "strategy_boxplot.png"))
plt.close()

print("✓ Analysis complete. Plots and stats saved.")