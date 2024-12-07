# Gluon

Gluon is a framework for test transplantation.

## Installation

- Install `miniconda` (depending on your OS)

- Run `./prepare-env.sh` to create the conda environment

- Run `conda activate gluon` to activate the environment

## Commands

All commands are run from the root directory of the project.

```bash
python \
    -m src.gluon.collect_tests.analyze_unit_tests \
    -i __internal__/_data/flask/ \
    -o __internal__/collected_tests_hybrid/v1/flask/ \
    > flask_tests_analysis_output.txt
```
