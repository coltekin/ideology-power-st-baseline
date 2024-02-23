#!/usr/bin/env python3
""" A simple baseline for the shared task on Ideology and Power Detection.

See the shared task web page <https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html>
for details.
"""
import argparse
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from data import get_data

ap = argparse.ArgumentParser()
ap.add_argument('parliaments', nargs="+")
ap.add_argument('--task', '-t', default='power')
ap.add_argument('--data-dir', '-d', default='data')
args = ap.parse_args()
args.parliaments = [x.lower() for x in args.parliaments]

for pcode in args.parliaments:
    # Train a logistic regression classifier, and pring evaluation
    # metrics on a held-out data split.
    start = time.time()
    train_file = os.path.join(args.data_dir, args.task,
                              f"{args.task}-{pcode}-train.tsv")
    if not os.path.exists(train_file):
        print(f"{pcode}: skipping, no training data.")
        continue
    t_trn, y_trn, t_val, y_val = get_data(train_file)
    vec = TfidfVectorizer(sublinear_tf=True, analyzer="char",
                          ngram_range=(1,3))
    x_trn = vec.fit_transform(t_trn)
    x_val = vec.transform(t_val)
    m = LogisticRegression()
    m.fit(x_trn, y_trn)
    pred = m.predict(x_val)
    p, r, f, _ = precision_recall_fscore_support(
            y_val, pred, average='macro', zero_division=0.0)
    print(f"{pcode}: {100*p:.4f} / {100*r:.4f} / {100*f:.4f}"
          f" [{time.time() - start:.2f}s]")

    # If the corresponding test file exists, create the submission
    # file with predictions.
    test_file = os.path.join(args.data_dir, args.task,
                              f"{args.task}-{pcode}-test.tsv")
    if os.path.exists(test_file):
        id_test, t_test = get_data(test_file, testset=True)
        x_test = vec.transform(t_test)
        test_pred = m.predict_proba(x_test)
        teamname = "baseline"
        pred_file = f"{teamname}-{args.task}-{pcode}-predictions.tsv"
        with open(pred_file, "wt") as fpred:
            for i, p in enumerate(test_pred):
                print(f"{id_test[i]}\t{p[1]}", file=fpred)
