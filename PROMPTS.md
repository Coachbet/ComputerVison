# AI usage and prompts

Tool used: Claude (Anthropic).
Below are the main prompts we used, grouped by task.


## Code and website
Built with Claude over several sessions; we no longer have the exact prompts.
Main requests: dataset loading, feature extraction, the HistGradientBoosting
model and its hyperparameters, unit tests, and the explanatory website.
- "Help me load the emoji dataset from train/ and train_labels.csv, matching images by Id"
- "Which HistGradientBoosting parameters should I use?


## Report review and understanding the model (Claude)

Review
- "Can you do a peer review on our report? Check if it fits the criteria of the professor and everything is coherent."
- "What were the errors that you flagged that didn't correspond to the project or the website?"
- "So you're saying these two tables don't say the same thing?"

## Understanding our own model
- "Explain gradient boosting really quickly."
- "Okay but does the model already know the answer in this case?"
- "What differs between max nodes and max number of turns? Isn't a node added each turn?"
- "What happens between each round? What results are used and for what? Explain the relation between max leaf and max iter."
- "What is an F1?"
- "What does the 350 correspond to again? Why this number?"

## Experiments
- "What does this part ask for?" (about measuring the score without Block A) → Claude wrote scripts/ablation.py, which we ran ourselves (0.960 → 0.866)
-  "Here is the result" → we ran it ourselves: 0.960 with all features, 0.866 without Block A 
- "Here is the result" → 4 misclassified images; Claude helped interpret why
  (file size, LA mode, Samsung-like export format)
-  "Does this mean I have to wait?" / "It's long" (a warning appeared while it ran)


## Report edits
- "What is missing here?" (about our model comparison table)
- "Where in the website does it show the results?"
  → we compared the website and the report ourselves
- "Is this normal?" (the image didn't display in Overleaf: missing package)
