#!/usr/bin/env python3
""" Read and return data for shared task on Ideology and Power Detection.

See shared task web page <https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html>
for details.
"""
import sys
import csv
csv.field_size_limit(sys.maxsize)
from sklearn.model_selection import train_test_split
from collections import Counter

def read_data(fname,
              task='orientation',
              testset=False,
              text_head='text',
              test_size=0.2,
              return_na=False,
              seed=None):
    """Read the test set or training set and split to train/val sets.

    Parameters:
    fname       The filename to read data from.
    task        'orientation', 'power' or 'populism'.
    testset     If True, return only (ids, texts, labels), no
                training/validation split is done, all labels will
                be -1 if the file does not include labels.
    text_head   The header of the text field,
                useful for reading the English translations.
    test_size   Size or ratio of the test data (see the documentation
                of scikit-learn train_test_split() for details). Note
                that the split is based on authors. The absolute size
                should be specified as the number of authors, and
                ratio will be approximate, it may diverge
                substantially depending on the number of speeches per author.
    return_na   Wheter to return the "NA" (not available) labels. If
                True, NA lables are returned as -1.
    seed        Random seed for reproducible output
    """
#    print('R:', fname, task)
    data = dict()
    with open(fname, "rt") as f:
        csv_r = csv.DictReader(f, delimiter="\t")
        for row in csv_r:
            label = row.get(task, 'NA')
            if  label == 'NA':
                if return_na: label = -1
                else: continue
            data[row['id']] = row
            data[row['id']][task] = int(label)


    if testset: # return only ID and text and label (all -1 if not available)
        if len(data) == 0:
            return [], [], []
        return zip(*[(x['id'], x[text_head], x[task]) for x in data.values()])

    # First, split the speakers to train/test sets such that
    # there are no overlap of the authors across the split.
    speakerdict = dict()
    for row in data.values():
        speakerdict[row['speaker']] = row[task]

    if len(speakerdict) == 0:
        print("No labels for the task {task}.")
        return [], [], [], []

    spklist   = list(speakerdict)
    labellist = [speakerdict[s] for s in speakerdict]

    stratify = labellist
    if len(set(spklist)) == 1: # single class
        print("Warning: only a single class.")

    if Counter(labellist).most_common()[-1][1] < 2:
        print("Warning: too few instances for some classes to do"
              " a stratified split.")
        stratify=None
    
    s_trn, s_val, _, _ = train_test_split(spklist, labellist,
                      test_size=test_size, stratify=stratify,
                      random_state=seed)
    s_val = set(s_val)
    # Now split the speeches based on speakers split above
    t_trn, t_val, y_trn, y_val = [], [], [], []
    for row in data.values():
        if row['speaker'] in s_val:
            t_val.append(row[text_head])
            y_val.append(row[task])
        else:
            t_trn.append(row[text_head])
            y_trn.append(row[task])
    return t_trn, y_trn, t_val, y_val

if __name__ == "__main__":
    a, b, c, d = read_data(sys.argv[1], task='power')
#    print(a, b, c, d)
