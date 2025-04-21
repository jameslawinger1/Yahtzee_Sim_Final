import pandas as pd
import numpy as np
import scipy.stats as stats
import os
import itertools
import csv # Add csv import

# --- Configuration ---
RESULTS_DIR = '../results' # Relative path to the results directory
OUTPUT_CSV_FILE = 'statistical_summary.csv' # Output file path
CONFIDENCE_LEVEL = 0.95
ALPHA = 0.05 # Significance level for hypothesis tests

# --- Helper Functions ---
def load_scores(strategy_name):
    """Loads scores for a given strategy from its CSV file."""
    filename = os.path.join(RESULTS_DIR, f"{strategy_name}_scores.csv")
    if not os.path.exists(filename):
        print(f"Warning: Results file not found for {strategy_name} at {filename}")
        return None
    try:
        df = pd.read_csv(filename)
        return df['score'].values
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def calculate_ci(data, confidence=0.95):
    """Calculates the confidence interval for the mean of the data."""
    n = len(data)
    # Handle potential empty data
    if n == 0:
        return np.nan, (np.nan, np.nan)
    mean = np.mean(data)
    sem = stats.sem(data) # Standard Error of the Mean
    if sem == 0 or np.isnan(sem): # Handle case with zero or nan standard error
        return mean, (mean, mean)
    # Use try-except for ppf calculation robustness
    try:
        margin_of_error = sem * stats.t.ppf((1 + confidence) / 2., n-1)
        if np.isnan(margin_of_error):
             return mean, (mean, mean) # Fallback if ppf fails
        return mean, (mean - margin_of_error, mean + margin_of_error)
    except Exception:
         return mean, (np.nan, np.nan) # Return NaN interval on error

# --- Main Analysis ---
print("Starting Statistical Analysis...")

# Find strategy names from the results directory
strategy_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith('_scores.csv')]
strategy_names = [f.replace('_scores.csv', '') for f in strategy_files]

if not strategy_names:
    print(f"Error: No strategy score files found in {RESULTS_DIR}. Please run the simulator first.")
    exit()

print(f"Found strategies: {', '.join(strategy_names)}")

# Load scores for all found strategies
all_scores = {}
for name in strategy_names:
    scores = load_scores(name)
    if scores is not None:
        all_scores[name] = scores

if not all_scores:
    print("Error: Failed to load scores for any strategy.")
    exit()

# --- Confidence Intervals ---
print("\n--- Confidence Intervals for Mean Score ---")
ci_results = {}
ci_data_for_csv = [] # List to store CI results for CSV
for name, scores in all_scores.items():
    mean, ci = calculate_ci(scores, CONFIDENCE_LEVEL)
    ci_results[name] = {'mean': mean, 'ci': ci}
    print(f"{name}: Mean = {mean:.2f}, {CONFIDENCE_LEVEL*100:.0f}% CI = ({ci[0]:.2f}, {ci[1]:.2f})")
    # Add results to list for CSV
    ci_data_for_csv.append({
        'Strategy': name,
        'Mean': f"{mean:.2f}",
        f'{CONFIDENCE_LEVEL*100:.0f}% Lower CI': f"{ci[0]:.2f}",
        f'{CONFIDENCE_LEVEL*100:.0f}% Upper CI': f"{ci[1]:.2f}"
    })

# --- Hypothesis Testing (Pairwise T-tests) ---
print(f"\n--- Pairwise Hypothesis Tests (t-test, alpha={ALPHA}) ---")
print("Null Hypothesis (H0): Mean scores are equal.")
print("Alternative Hypothesis (Ha): Mean scores are different.")

ht_data_for_csv = [] # List to store hypothesis test results for CSV

# Compare all pairs of strategies
# Use sorted keys to ensure consistent comparison order if script is run multiple times
strategy_keys = sorted(all_scores.keys())
for name1, name2 in itertools.combinations(strategy_keys, 2):
    scores1 = all_scores[name1]
    scores2 = all_scores[name2]

    # Perform independent two-sample t-test
    t_stat, p_value = stats.ttest_ind(scores1, scores2, equal_var=False, nan_policy='omit') # Add nan_policy

    print(f"\nComparing {name1} vs {name2}:")
    print(f"  t-statistic = {t_stat:.3f}")
    print(f"  p-value = {p_value:.4f}")

    significant = p_value < ALPHA
    conclusion = ""
    if significant:
        mean1 = ci_results[name1]['mean']
        mean2 = ci_results[name2]['mean']
        # Handle potential NaN means for comparison
        if np.isnan(mean1) or np.isnan(mean2):
            conclusion = "Statistically significant difference (means cannot be compared due to NaN)."
            print(f"  Result: Reject H0. There is a statistically significant difference.")
            print(f"  Conclusion: {conclusion}")
        else:
            winner = name1 if mean1 > mean2 else name2
            loser = name2 if mean1 > mean2 else name1
            conclusion = f"Statistically significant difference. {winner}'s mean ({mean1:.2f}) is higher than {loser}'s ({mean2:.2f})."
            print(f"  Result: Reject H0. There is a statistically significant difference.")
            print(f"  Conclusion: {winner}'s mean score ({mean1:.2f}) is significantly higher than {loser}'s ({mean2:.2f}).")

    else:
        conclusion = "No statistically significant difference found."
        print(f"  Result: Fail to reject H0. No statistically significant difference found.")

    # Add results to list for CSV
    ht_data_for_csv.append({
        'Strategy 1': name1,
        'Strategy 2': name2,
        'T-Statistic': f"{t_stat:.3f}",
        'P-Value': f"{p_value:.4g}", # Use general format for p-value
        f'Significant (alpha={ALPHA})': significant,
        'Conclusion': conclusion
    })

# --- Save Results to CSV ---
try:
    with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        # Write Confidence Intervals
        if ci_data_for_csv:
            ci_fieldnames = ci_data_for_csv[0].keys()
            ci_writer = csv.DictWriter(csvfile, fieldnames=ci_fieldnames)
            csvfile.write("--- Confidence Intervals ---\n") # Section Header
            ci_writer.writeheader()
            ci_writer.writerows(ci_data_for_csv)
            csvfile.write("\n") # Add blank line separator
        else:
            csvfile.write("--- No Confidence Interval Data ---\n\n")

        # Write Hypothesis Tests
        if ht_data_for_csv:
            ht_fieldnames = ht_data_for_csv[0].keys()
            ht_writer = csv.DictWriter(csvfile, fieldnames=ht_fieldnames)
            csvfile.write("--- Pairwise Hypothesis Tests ---\n") # Section Header
            ht_writer.writeheader()
            ht_writer.writerows(ht_data_for_csv)
        else:
             csvfile.write("--- No Hypothesis Test Data ---\n")

    print(f"\nAnalysis results successfully saved to {OUTPUT_CSV_FILE}")

except Exception as e:
    print(f"\nError saving results to CSV file {OUTPUT_CSV_FILE}: {e}")

print("\nAnalysis Complete.") 