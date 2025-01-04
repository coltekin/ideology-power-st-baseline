#!/usr/bin/env python3
""" Read and return data for shared task on Ideology and Power Detection.

See shared task web page <https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html>
for details.
"""
import sys
import csv
csv.field_size_limit(sys.maxsize)
from sklearn.model_selection import train_test_split

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
    task        'orientation', 'power', 'populism', or 'all'. If set
                to 'all', the argument return_na is ignored.
    testset     If True, return only (ids, texts, labels), no
                training/validation split is done, all labels will
                be -1 if the file does not include labels.
    text_head   The header of the text field,
                useful for reading the English translations.
    test_size   Size or ratio of the test data (see the documentation
                of scikit-learn train_test_split() for details)
    return_na   Wheter to return the "NA" (not available) labels. If
                True, NA lables are returned as -1.
    seed        Random seed for reproducible output
    """
    data = []
    with open(fname, "rt") as f:
        csv_r = csv.DictReader(f, delimiter="\t")
        for row in csv_r:
            data.append(row)

    ids = [x['id'] for x in data]
    texts = [x[text_head] for x in data]
    labels = []
    for row in data:
        if task == 'all':
            l = []
            for t in ('orientation', 'power', 'populism'):
                try: v = int(row.get(t))
                except: v = -1
                l.append(v)
            labels.append(tuple(l))
        else:
            try: v = int(row.get(task))
            except: v = -1
            labels.append(v)

    if testset: # return only ID and text and label (all -1 if not available)
        return (ids, texts, labels)

    # First, split the speakers to train/test sets such that
    # there are no overlap of the authors across the split.
    # This is similar to how orientation test set was split.
    spkset, labelset = [], []
    for i, row in enumerate(data):
        if not return_na and task != "all" and labels[i] == -1:
            continue
        if row['speaker'] not in spkset:
            spkset.append(row['speaker'])
            labelset.append(labels[i])
    if len(spkset) == 0:
        return [], [], [], []
    s_trn, s_val, _, _ = train_test_split(spkset, labelset,
                      test_size=test_size, stratify=labelset,
                      random_state=seed)
    s_val = set(s_val)
    # Now split the speeches based on speakers split above
    t_trn, t_val, y_trn, y_val = [], [], [], []
    for i, row in enumerate(data):
        if row['speaker'] in s_val:
            t_val.append(texts[i])
            y_val.append(labels[i])
        else:
            t_trn.append(texts[i])
            y_trn.append(labels[i])
    return t_trn, y_trn, t_val, y_val

if __name__ == "__main__":
    a, b, c, d = read_data(sys.argv[1], task='populism')
    print(len(a), len(b), len(c), len(d))
    read_data(sys.argv[1], task="all")
