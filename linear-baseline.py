#!/usr/bin/env python3
""" A simple baseline for the shared task on Ideology and Power Detection.

See the shared task web page <https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html>
for details.
"""
import argparse
import os
import time
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from data import get_data
import numpy as np
from multiprocessing import Pool

ap = argparse.ArgumentParser()
ap.add_argument('parliaments', nargs="+")
ap.add_argument('--task', '-t', default='power',
        choices=['power', 'orientation'])
ap.add_argument('--data-dir', '-d', default='data')
ap.add_argument('--C', '-C', type=int, default=1)
ap.add_argument('--repeat', '-r', type=int, default=1)
ap.add_argument('--nproc', '-j', type=int, default=4)
ap.add_argument('--en-translation', '-e', action='store_true')
ap.add_argument('--pred-dir', '-p', default='predictions')
ap.add_argument('--save-models', '-s', default='models')
ap.add_argument('--load-models', '-l')
ap.add_argument('--teamname', '-T', default="baseline")
args = ap.parse_args()
args.parliaments = [x.lower() for x in args.parliaments]

if args.parliaments[0] == "all":
    args.parliaments = ["at", "ba", "be", "bg", "cz", "dk", "ee",
                        "es-ct", "es-ga", "es-pv", "es", "fi", "fr",
                        "gb", "gr", "hr", "hu", "is", "it", "lv",
                        "nl", "no", "pl", "pt", "rs", "se", "si",
                        "tr", "ua"]

def predict(pcode):
    def write_predictions(m):
        # If the corresponding test file exists, create the submission
        # file with predictions.
        test_file = os.path.join(args.data_dir, args.task,
                                  f"{args.task}-{pcode}-test.tsv")
        if os.path.exists(test_file):
            id_test, t_test, _ = get_data(test_file, testset=True)
            x_test = vec.transform(t_test)
            test_pred = m.predict_proba(x_test)
            pred_file = f"{args.teamname}-{args.task}-{pcode}-predictions.tsv"
            os.makedirs(args.pred_dir, exist_ok=True)
            with open(os.path.join(args.pred_dir, pred_file), "wt") as fpred:
                for i, p in enumerate(test_pred):
                    print(f"{id_test[i]}\t{p[1]}", file=fpred)
    if args.load_models:
        try:
            model_file = f"{args.task}-{pcode}.joblib"
            vec, m = joblib.load(
                    os.path.join(args.load_models, model_file))
        except:
            m = None
            print("Failed to read model from "
                 f"{args.load_models}/{model_file}.")
        if m: write_predictions(m)
    else:
        # Train a logistic regression classifier, and print evaluation
        # metrics on a held-out data split.
        start = time.time()
        train_file = os.path.join(args.data_dir, args.task,
                                  f"{args.task}-{pcode}-train.tsv")
        if not os.path.exists(train_file):
            print(f"{pcode}: skipping, no training data.")
            return
        P, R, F = [], [], []
        best_F = 0.0
        for i in range(args.repeat):
            if pcode != "gb" and args.en_translation:
                t_trn, y_trn, t_val, y_val = get_data(train_file,
                        text_head='text_en')
            else:
                t_trn, y_trn, t_val, y_val = get_data(train_file)
            vec = TfidfVectorizer(sublinear_tf=True, analyzer="char",
                                  ngram_range=(1,3))
            x_trn = vec.fit_transform(t_trn)
            x_val = vec.transform(t_val)
            m = LogisticRegression(max_iter=500, C=args.C)
            m.fit(x_trn, y_trn)
            pred = m.predict(x_val)
            p, r, f, _ = precision_recall_fscore_support(
                    y_val, pred, average='macro', zero_division=0.0)
            P.append(p), R.append(r), F.append(f)

            if f > best_F:
                if args.save_models:
                    os.makedirs(args.save_models, exist_ok=True)
                    joblib.dump((vec, m), os.path.join(args.save_models,
                        f"{args.task}-{pcode}.joblib"))
                write_predictions(m)
            if args.repeat == 1:
                p, r, f = P[0], R[0], F[0]
                print(f"{pcode}: {100*p:.4f} / {100*r:.4f} / {100*f:.4f}"
                      f" [{time.time() - start:.2f}s]")
            else:
                p, psd = np.mean(P), np.std(P)
                r, rsd = np.mean(R), np.std(R)
                f, fsd = np.mean(F), np.std(F)
                print(f"{pcode}: {100*p:.4f}±{100*psd:.4f} "
                      f"{100*r:.4f}±{100*rsd:.4f} "
                      f"{100*f:.4f}±{100*fsd:.4f} "
                      f" [{(time.time() - start) / len(P):.2f}s]")

pool = Pool(processes=args.nproc)
pool.map(predict, args.parliaments)
