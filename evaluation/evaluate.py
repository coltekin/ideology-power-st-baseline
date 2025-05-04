#!/usr/bin/env python3

import argparse
import os
import sys
import glob
import re
import csv
import numpy as np
from sklearn.metrics import precision_recall_fscore_support
from tira.io_utils import to_prototext
from parliaments import parl_task

GOLD = os.environ.get('inputDataset', 'reference')
PRED = os.environ.get('inputRun', 'predictions')
OUTD = os.environ.get('outputDir', '.')

pred_re = re.compile(
    r"(?P<team>[^-]+)-(?P<task>[^-]+)-(?P<parl>[^-]{2}(-[^-]{2})?)-(?P<run>[^-]+)\.tsv")


def score(pred, task, parl, refdir=GOLD):
    goldfile = os.path.join(refdir,
            '-'.join((task, parl, 'test-labels')) + '.tsv')
    goldids, goldlabels = [], []
    with open(goldfile, 'rt') as f:
        csvr = csv.reader(f, delimiter='\t')
        _ = next(csvr)
        for row in csvr:
            id_, lab = row
            if lab == 'NA': continue
            goldids.append(id_)
            goldlabels.append(int(lab))

    predlabels = [round(pred[i]) for i in goldids]

    p, r, f, supp = precision_recall_fscore_support(
            goldlabels, predlabels, average='macro',
            zero_division=0.0)
    return p, r, f

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument('--reference', '-r', default=GOLD)
    ap.add_argument('--predictions', '-p', default=PRED)
    ap.add_argument('--outdir', '-o', default=OUTD)
    args = ap.parse_args()


    print(args.reference, args.predictions, args.outdir)
    print(glob.glob(args.predictions + '/*'))

    tasks = ('power', 'orientation', 'populism')
    scores = dict()
    predfiles = os.path.join(args.predictions, "*")
    for predfile in glob.glob(predfiles):
        fname = os.path.basename(predfile)
        if not os.path.isfile(predfile) and os.path.getsize(predfile) == 0:
            print(f"Skipping {fname}, no content.", file=sys.stderr)
            continue
        elif fname.lower().startswith('readme'): # skip quietly
            continue
        m = pred_re.match(fname)
        if not m:
            print(f"Skipping {fname}: file name pattern does not match.",
                    file=sys.stderr)
            continue
        team, task = m.group('team'), m.group('task')
        parl, run =  m.group('parl'), m.group('run')
        if task not in tasks:
            print(f"Skipping {fname}:", end=" ", file=sys.stderr)
            print(f"Unknown task or parliament or task '{task}'.",
                  file=sys.stderr)
        if not parl_task[parl][task]:
            print(f"Skipping {fname}:", end=" ", file=sys.stderr)
            print(f"Task {task} is not available for parliament '{parl}'.",
                  file=sys.stderr)
            continue
        print(f"Procesing {fname}.")
#        try:
        with open(predfile, 'rt') as f:
            pred = dict()
            for line in f:
                id_, prob = line.strip().split('\t')
                pred[id_] = float(prob)
        scores[(task, parl)] = score(pred, task, parl,
                                         refdir=args.reference)
#        except:
#            print(f'Wrong file format {predfile}.', file=sys.stderr)
#            print('All rows of the prediction files should contain'
#                  'two columns(id, class/score) separated with a single tab.',
#                  file=sys.stderr)

    if len(scores) == 0:
        print(f'None of the input files are valid. No scores calcualted',
                file=sys.stderr)
        sys.exit(-1)

    with open(os.path.join(args.outdir, 'evaluation.prototext'), 'wt') as outf:
        ret = {}
        ori_f, pow_f, pop_f = 0.0, 0.0, 0.0
        pscores = [scores[x] for x in scores if x[0] == 'power']
        if len(pscores) > 0:
            pow_p, pow_r, pow_f = np.mean(pscores, axis=0)
        popscores = [scores[x] for x in scores if x[0] == 'populism']
        if len(popscores) > 0:
            pop_p, pop_r, pop_f = np.mean(popscores, axis=0)
        oscores = [scores[x] for x in scores if x[0] == 'orientation']
        if len(oscores) > 0:
            ori_p, ori_r, ori_f = np.mean(oscores, axis=0)
        ret['F1_orientation'] = ori_f
        ret['F1_populism'] = pop_f
        ret['F1_power'] = pow_f
        for sc in sorted(scores):
            task, parl = sc
            for k, m in zip(("Precision", "Recall", "F1"), scores[sc]):
                ret[f'{k}_{task}_{parl.upper()}'] = m
         
        outf.write(to_prototext([ret]))

