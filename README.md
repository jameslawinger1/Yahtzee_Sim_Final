# Yahtzee Strategy Simulation – ISYE 6644

This project simulates games of Yahtzee using several strategies to evaluate their performance via Monte Carlo simulation. The objective is to determine which strategy scores highest on average over many games.

---

## How to Run

1. **Run all strategy simulations:**
```bash
python yahtzee_simulator.py
```

2. **Generate statistical plots and summary metrics:**
```bash
python analysis.py
```

3. **Perform head-to-head strategy comparison:**
```bash
python head_to_head.py
```

Results and plots will be saved to `results/` and `plots/` directories, which are auto-created.

---

## File Descriptions

### Core Simulation Files
- **`yahtzee_simulator.py`**: Main script for running simulations across all strategies. Computes average scores, saves results to CSV.
- **`scoreboard.py`**: Scoring rules for each Yahtzee category.
- **`dice_rolling.py`**: Manages dice rolling and rerolling logic.

### Strategy Modules (in `strategies/` folder)
- **`greedy_strategy.py`**: Always picks the category with the highest score after each roll.
- **`upper_focus_strategy.py`**: Focuses on maximizing upper section scores (1s-6s) to earn the 35-point bonus.
- **`lower_focus_strategy.py`**: Prioritizes scoring lower section categories (e.g., straights, full house, Yahtzee).
- **`yahtzee_focus_strategy.py`**: Aggressively targets Yahtzee rolls even at the expense of consistency.
- **`dice_driven_strategy.py`**: Dynamically chooses a strategy based on the initial roll each turn.

### Analysis & Evaluation
- **`analysis.py`**: Computes summary statistics (mean, median, standard deviation, confidence intervals), and generates histograms and a boxplot for all strategies.
- **`head_to_head.py`**: Simulates head-to-head comparisons between all strategies, saves win rate matrix, and plots a heatmap.

### Outputs
- **`results/`**: Stores CSV files with raw scores, summary stats, and head-to-head win matrix.
- **`plots/`**: Stores visualizations such as histograms, boxplots, and heatmaps.


## Requirements
- Python 3.x
- Packages: `numpy`, `pandas`, `matplotlib`

Install dependencies via pip:
```bash
pip install numpy pandas matplotlib
```

---

## Authors
Kevin Bai, James Lawinger  
ISYE 6644 - Group 44  
Spring 2025

---

## References
- https://pi.math.cornell.edu/~mec/2006-2007/Probability/Yahtzee.htm
- https://en.wikipedia.org/wiki/Yahtzee
- https://solitaired.com/guides/yahtzee-strategy
- https://www.dumbthoughtsthatmakemelaugh.com/blog/yahtzee-strategy
- http://www.yahtzee.org.uk/strategy.html
- https://chat.openai.com/ (Used for code refinement and documentation)

