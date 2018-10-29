[![DOI](https://zenodo.org/badge/94531811.svg)](https://zenodo.org/badge/latestdoi/94531811)

# pycoQC_2 package documentation

---

**PycoQC is a Python 3 package for Jupyter Notebook, computing metrics and generating simple QC plots
from the sequencing summary report generated by Oxford Nanopore technologies Albacore basecaller**

---

pycoQC_2 is a very simple quality control package for Nanopore data written in pure **python3**, meant
to be used directly in a **jupyter notebook** 4.0.0 +.
As opposed to more exhaustive QC programs for nanopore data, pycoQC is very fast as it relies entirely on the *sequencing_summary.txt* file generated by ONT Albacore
Sequencing Pipeline Software, during basecalling. Consequently, pycoQC will only provide metrics at read level
metrics (and not at base level). The package supports 1D and 1D2 runs analysed with Albacore.

PycoQC requires the following fields in the sequencing.summary.txt file:

* 1D run => **read_id**, **run_id**, **channel**, **start_time**, **sequence_length_template**, **mean_qscore_template**
* 1D2 run =>**read_id**, **run_id**, **channel**, **start_time**, **sequence_length_2d**, **mean_qscore_2d**

In addition it will try to get the following optional fields if they are available:

* **calibration_strand_genome_template**, **barcode_arrangement**

---

* Author: Adrien Leger - aleg@ebi.ac.uk

* URL: https://github.com/a-slide/pycoQC

* Licence: GPLv3

* Python version: >=3.3


# Installation

Ideally, before installation, create a clean python3 virtual environment to deploy the package, using virtualenvwrapper for example (see http://www.simononsoftware.com/virtualenv-tutorial-part-2/).

## Dependencies

PycoQC relies on a few Python third party libraries. The correct versions of packages are installed together with the software when using pip.

## Option 1: Direct installation with pip from github (recommended)

Install the package with pip3. Python dependencies will be automatically installed.

`pip3 install git+https://github.com/a-slide/pycoQC.git`

To update the package:

`pip3 install git+https://github.com/a-slide/pycoQC.git --upgrade`


## Option 2: Clone the repository and install locally in develop mode

With this option, the package will be locally installed in “editable” or “develop” mode. This allows the package to be both installed and editable in project form. This is the recommended option if you wish to participate to the development of the package. Python dependencies will be automatically installed.

`git clone https://github.com/a-slide/pycoQC.git`

`cd pycoQC`

`chmod u+x setup.py`

`pip3 install -e ./`

# Jupyter Notebook Usage

The package is meant to be used in a jupyter notebook 4.0.0 +

## Interactive demo notebook

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/a-slide/pycoQC/dev?filepath=tests%2FpycoQC_usage.ipynb)

## Static demo notebook

[]()

## Running your own notebook locally

Launch the notebook in a shell terminal

`jupyter notebook`

If it does not autolaunch your web browser, open manually the following URL http://localhost:8888/tree

From Jupyter home page you can navigate to the directory you want to work in. Then, create a new Python3 Notebook.

# Note to power-users and developers

Please be aware that pycoQC is an experimental package that is still under development. It was tested under Linux Ubuntu 16.04 and in an HPC environment running under Red Hat Enterprise 7.1.

You are welcome to contribute by requesting additional functionalities, reporting bugs or by forking and submitting pull requests

Thank you

### Acknowledgments

Thanks to [Kim Judge](https://twitter.com/kim_judge_) for providing a few example sequencing summary files.
