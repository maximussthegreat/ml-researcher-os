# Synthetic Paper Excerpt

We propose TinyDense, a compact classifier for short clinical notes. TinyDense improves macro F1 by 3.2 points over a logistic regression baseline on a private dataset of 8,000 notes.

The model uses a small transformer encoder followed by mean pooling and a two-layer MLP. We train for 10 epochs with AdamW. We report the best validation checkpoint.

We do not evaluate on an external dataset. Hyperparameters were selected manually. We leave robustness to longer notes for future work.

