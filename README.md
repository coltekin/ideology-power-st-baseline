## Baseline and evaluation script for the shared task on [Ideology and Power Identification in Parliamentary Debates](https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html)

This repository contains a simple linear baseline, and example
submission file  for the shared task on [Ideology and Power
Identification in Parliamentary Debates](https://touche.webis.de/clef24/touche24-web/ideology-and-power-identification-in-parliamentary-debates.html).

Please join [the shared task
mailing](https://groups.google.com/g/ideology-and-power-in-parliamentary-speeches)
list for announcements.

The baseline assumes that the training and test data is placed at
`data/` subdirectory. The training and test dataset for the shared
task are proved at <https://zenodo.org/doi/10.5281/zenodo.10450640>
and <https://zenodo.org/doi/10.5281/zenodo.11061649>. 
We also provide a jupyter-notebook version (not fully complete)
of the baseline.

To train the baseline with the command line version of the baseline on
all datasets and all parliaments, you can use:

```
python3 linear-baseline.py -s models -t power -t orientation -p output all
```
This will also save the trained models under `models/`,
and test file predictions under `output/`. You can zip the files under
`output/` and submit as a run to
[submission system](https://www.tira.io/task-overview/ideology-and-power-identification-in-parliamentary-debates-2024).

You can alternatively create a docker file with
```
docker build -t ideology-powerbaseline:0.0.1 .
```
and make a docker submission. The docker setup assumes that you
trained the models, and saved them under `models/`.

For further examples for docker submissions, you can also have a look
at the [Human Value Detection Shared Task baslines](https://github.com/touche-webis-de/touche-code/tree/main/clef24/human-value-detection/approaches)
which include a more varied set of approaches.
