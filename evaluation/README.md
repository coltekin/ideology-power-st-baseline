# Evaluator for the shared task

This directory contains the evaluation script for the
[Ideology and Power Identification in Parliamentary
Debates](https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html)
shared task.

The evaluation script `evaluate.py` can be run either stand alone,
or through TIRA.


The predictions should be formatted as simple TSV files with two
columns, `id`, and the `prediction`. The prediction files should _not_
contain a header row. The names of the files should be formatted
according following template:

```
<team>-<task>-<pcode>-<runname>.tsv
```
The `<task>` is either `orientation`, or `power`, and the `<pcode>`
is the lowercase code of the parliament (e.g., `at`, or `es-ct`).
The `<team>` and `<runname>` can be helpful for identifying the team
and the approach or the run information, but they are not significant
for the evaluation script. You can set them to arbitrary strings, 
but they cannot be empty, and they should not contain a dash (`-`).
All files should be placed in the same directory/folder without
further directory hierarchy. If you are participating in only a subset of
the tasks and/or parliaments, then you can submit files only for the
combinations that you participate in.

The directory `toy-predictions` in this repository provides a toy
submission example. To submit the run, you should create a zip archive
with the contents of the direcotry (only files, without additional
folders/directories) and submit your run through web interface at
<https://www.tira.io/task-overview/ideology-and-power-identification-in-parliamentary-debates-2024>
or thorough CLI as instructed in the submission web page.

## Running the evaluator locally

Evaluation script needs both the predictions (run) and the
gold-standard labels. If you want to experiment with the toy dataset,
or the validation split you use for development, you can run the
command evaluation command similar to:
```
python3 evaluate.py -p toy-predictions -r toy-labels
```
The above command should work for the toy dataset (which includes some
intentional mistakes). The scores are written to a file with name
`evaluation.prototext`.

## Running the evaluator locally through TIRA

With [tira client](https://pypi.org/project/tira/), and
[docker](docker.io) installed, you can also run the evaluator as it
will be run on tira locally using the the following command:

```
tira-run --input-run $PWD/toy-predictions \
         --input-directory $PWD/toy-labels \
         --image coltekin/ideology-power-st-evaluator:0.0.6 \
         --output-directory $PWD/output \
         --command /evaluate.py
```
This will write the scores in directory `output/evaluation.prototext`.

