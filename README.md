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

## Submit to TIRA via Code-Submissions

First, please ensure that your have a valid tira client installed via:

```
pip3 install --upgrade tira
tira-cli verify-installation
```

Next, please test that your approach works on the toy dataset as expected (more details are available in the [documentation](https://docs.tira.io/participants/participate.html#submitting-your-submission)):

```
tira-cli code-submission --dry-run --path . --task ideology-and-power-identification-in-parliamentary-debates-2025 --dataset ideology-and-power-toy-dataset-20250505-training --command 'python3 /linear-baseline.py -l /models -t power -t orientation -t populism -p $outputDir -d $inputDataset all'
```

If this works as expected, you can omit the `--dry-run` argument to submit this baseline to TIRA, please run:

```
tira-cli code-submission --path . --task ideology-and-power-identification-in-parliamentary-debates-2025 --dataset ideology-and-power-toy-dataset-20250505-training --command 'python3 /linear-baseline.py -l /models -t power -t orientation -t populism -p $outputDir -d $inputDataset all'
```

## Submit to TIRA via Run-Submissions

Assuming you have made predictions for the test dataset in a directory `test-outputs`, you can upload via the command line:


```
pip3 install --upgrade tira
tira-cli login --token YOUR-TOKEN-FROM-THE-UI
tira-cli verify-installation

tira-cli upload --dataset ideology-and-power-identification-20250504-test --directory test-outputs --system THE-NAME-OF-YOUR-SYSTEM
```

Alternatively, you can upload your data as a zip directory in the UI.
