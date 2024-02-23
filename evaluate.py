#!/usr/bin/env python3
""" Evaluation script for the shared task on Ideology and Power Detection.

See the shared task web page <https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html>
for details.
"""
import argparse
import os
from sklearn.metrics import precision_recall_fscore_support
from data import get_data

ap = argparse.ArgumentParser()
ap.add_argument('gold')
ap.add_argument('pred')
args = ap.parse_args()


gids, _, glabels = get_data(args.gold, testset=True)

with open(args.pred, 'rt') as f:
    pids, pred_scores = [], []
    for line in f:
        id_, score = line.strip().split()
        score = float(score)
        pids.append(id_)
        pred_scores.append(score)
pred_labels = [0 if score < 0.5 else 1 for score in pred_scores]
pred_scores = dict(zip(pids, pred_scores))
pred_labels = dict(zip(pids, pred_labels))

pred = [pred_labels[i] for i in gids]

p, r, f, _ = precision_recall_fscore_support(
        glabels, pred, average='macro', zero_division=0.0)
print(f"{100*p:.4f} / {100*r:.4f} / {100*f:.4f}")
