![pycoQC](https://raw.githubusercontent.com/a-slide/pycoQC/master/docs/pictures/pycoQC_long.png)

[![JOSS](http://joss.theoj.org/papers/ea8e08dc950622bdd5d16a65649954aa/status.svg)](http://joss.theoj.org/papers/ea8e08dc950622bdd5d16a65649954aa)
[![DOI](https://zenodo.org/badge/94531811.svg)](https://zenodo.org/badge/latestdoi/94531811)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/pycoQC/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link)
[![GitHub license](https://img.shields.io/github/license/a-slide/pycoQC.svg)](https://github.com/a-slide/pycoQC/blob/master/LICENSE)
[![Language](https://raw.githubusercontent.com/a-slide/pycoQC/master/docs/pictures/language-Python3-brightgreen.png)](https://www.python.org/)

[![PyPI version](https://badge.fury.io/py/pycoQC.svg)](https://badge.fury.io/py/pycoQC)
[![Downloads](https://pepy.tech/badge/pycoqc)](https://pepy.tech/project/pycoqc)
[![Anaconda Version](https://anaconda.org/aleg/pycoqc/badges/version.svg)](https://anaconda.org/aleg/pycoqc)
[![Anaconda Downloads](https://anaconda.org/aleg/pycoqc/badges/downloads.svg)](https://anaconda.org/aleg/pycoqc)

[![Build Status](https://travis-ci.com/a-slide/pycoQC.svg?branch=master)](https://travis-ci.com/a-slide/pycoQC)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/07db58961a3c4fc1b6dc34c54079b477)](https://www.codacy.com/app/a-slide/pycoQC?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=a-slide/pycoQC&amp;utm_campaign=Badge_Grade)
---

**Full documentation is available at https://a-slide.github.io/pycoQC/**

---

**PycoQC computes metrics and generates interactive QC plots for Oxford Nanopore technologies sequencing data**

PycoQC relies on the *sequencing_summary.txt* file generated by Albacore and Guppy, but if needed it can also generates a summary file from basecalled fast5 files. The package supports 1D and 1D2 runs generated with Minion, Gridion and Promethion devices and basecalled with Albacore 1.2.1+ or Guppy 2.1.3+. PycoQC is written in pure Python3. **Python 2 is not supported**.

## Gallery

![summary](./docs/pictures/summary.gif)

![reads_len_1D_example](./docs/pictures/reads_len_1D.gif)]

![reads_len_1D_example](./docs/pictures/reads_qual_1D.gif)]

![reads_qual_len_2D_example](./docs/pictures/reads_qual_len_2D.gif)

![channels_activity](./docs/pictures/channels_activity.gif)

![output_over_time](./docs/pictures/output_over_time.gif)

![qual_over_time](./docs/pictures/qual_over_time.gif)

![len_over_time](./docs/pictures/len_over_time.gif)

![align_len](./docs/pictures/align_len_1D.gif)

![align_score](./docs/pictures/align_score_1D.gif)

![align_score_len_2D](./docs/pictures/align_score_len_2D.gif)

![alignment_coverage](./docs/pictures/alignment_coverage.gif)

![alignment_rate](./docs/pictures/alignment_rate.gif)

![alignment_summary](./docs/pictures/alignment_summary.gif)

## Example HTML reports

* [Albacore_all_RNA](https://a-slide.github.io/pycoQC/pycoQC/results/Albacore_all_RNA.html)

* [Guppy-2.1.3_basecall-1D_RNA](https://a-slide.github.io/pycoQC/pycoQC/results/Guppy-2.1.3_basecall-1D_RNA.html)

* [Guppy-2.3_basecall-1D_alignment-DNA](https://a-slide.github.io/pycoQC/pycoQC/results/Guppy-2.3_basecall-1D_alignment-DNA.html)

* [Albacore-1.2.1_basecall-1D-DNA](https://a-slide.github.io/pycoQC/pycoQC/results/Albacore-1.2.1_basecall-1D-DNA.html)

* [Guppy-2.1.3_basecall-1D_DNA_barcode](https://a-slide.github.io/pycoQC/pycoQC/results/Guppy-2.1.3_basecall-1D_DNA_barcode.html)

* [Albacore-1.7.0_basecall-1D-DNA_API](https://a-slide.github.io/pycoQC/pycoQC/results/Albacore-1.7.0_basecall-1D-DNA_API.html)

* [Albacore-2.1.10_basecall-1D-DNA](https://a-slide.github.io/pycoQC/pycoQC/results/Albacore-2.1.10_basecall-1D-DNA.html)

* [Albacore-1.7.0_basecall-1D-DNA](https://a-slide.github.io/pycoQC/pycoQC/results/Albacore-1.7.0_basecall-1D-DNA.html)

## Example JSON reports

* [Guppy-2.3_basecall-1D_alignment-DNA](https://a-slide.github.io/pycoQC/pycoQC/results/Guppy-2.3_basecall-1D_alignment-DNA.json)

* [Guppy-2.1.3_basecall-1D_RNA](https://a-slide.github.io/pycoQC/pycoQC/results/Guppy-2.1.3_basecall-1D_RNA.json)

* [Albacore-1.7.0_basecall-1D-DNA_API](https://a-slide.github.io/pycoQC/pycoQC/results/Albacore-1.7.0_basecall-1D-DNA_API.json)

## Authors

* Adrien Leger - aleg {at} ebi.ac.uk

* Tommaso Leonardi - tom {at} tleo.io
