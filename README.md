## Baseline and evaluation script for the shared task on [Ideology and Power Identification in Parliamentary Debates](https://touche.webis.de/clef25/touche25-web/ideology-and-power-identification-in-parliamentary-debates.html)

This repository contains baseline and evaluation scripts
for the 2025 edition of the [Ideology and Power Identification in Parliamentary Debates](https://touche.webis.de/clef25/touche25-web/ideology-and-power-identification-in-parliamentary-debates.html).
For 2024 edition of the shared task repository please visit 
<https://github.com/coltekin/ideology-power-st-baseline/tree/2024>.
For annoucementa, please join mailing lists for the [shared task](https://groups.google.com/g/ideology-and-power-in-parliamentary-speeches)
and the [lab](https://groups.google.com/g/touche-lab) for announcements.

The baseline assumes that the training and test data is placed at
`data/` subdirectory. The training dataset for the shared
task is proved at <https://doi.org/10.5281/zenodo.14600017>.

To train the baseline with the command line version of the baseline on
all datasets and all parliaments, you can use:

```
python3 linear-baseline.py -s models -t power -t orientation -t populism -p output all
```
This will also save the trained models under `models/`,
and test file predictions under `output/`,
which are in the expected format for the submission.
To run the baseline on the trial data add `-d sample-data` to the
command line.
Further information on submission system will be provided soon.
