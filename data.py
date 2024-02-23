#!/usr/bin/env python3
""" Read and return data for shared task on Ideology and Power Detection.

See shared task web page <https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html>
for details.
"""
import sys
import csv
csv.field_size_limit(sys.maxsize)
from sklearn.model_selection import train_test_split

def get_data(fname, testset=False, text_head='text', test_size=0.2, seed=None):
    """Read the test set or training set and split to train/val sets.

    Parameters:
    fname       The filename to read data from.
    testset     If True, return only (ids, texts, labels), no
                training/validation split is done, all labels will
                be -1 if the file does not include labels.
    text_head   The header of the text field,
                useful for reading the English translations.
    test_size   Size or ratio of the test data (see the documentation
                of scikit-learn train_test_split() for details)
    seed        Random seed for reproducible output
    """
    texts, speaker_label = [], dict()
    with open(fname, "rt") as f:
        csv_r = csv.DictReader(f, delimiter="\t")
        for row in csv_r:
            texts.append((row['id'], row['speaker'], row[text_head]))
            speaker_label[row['speaker']] = int(row.get('label', -1))

    if testset: # return only ID and text and label
        return ([x[0] for x in texts],
                [x[2] for x in texts],
                [speaker_label[x[1]] for x in texts])

    # First, split the speakers to train/test sets such that
    # there are no overlap of the authors across the split.
    # This is similar to how orientation test set was split.
    spkset = list(speaker_label.keys())
    labelset = list(speaker_label.values())
    s_trn, s_val, _, _ = train_test_split(spkset, labelset,
                      test_size=test_size, random_state=seed)
    s_val = set(s_val)
    # Now split the speeches based on speakers split above
    t_trn, t_val, y_trn, y_val = [], [], [], []
    for i, (_, spk, text) in enumerate(texts):
        if spk in s_val:
            t_val.append(text)
            y_val.append(speaker_label[spk])
        else:
            t_trn.append(text)
            y_trn.append(speaker_label[spk])
    return t_trn, y_trn, t_val, y_val
