# Gluon

Gluon is a framework for test transplantation.

[Notion notes](https://childlike-feeling-7e1.notion.site/Recap-1768e948699d80d2ba9bffcc5b07523d?pvs=4)

## Experimental Setup

Set up the repos and run the tests. Check the logs if there are any installation issues.

```bash
./pipeline.sh
```

## Installation

- Install `miniconda` (depending on your OS)

- Run `./prepare-env.sh` to create the conda environment

- Run `conda activate gluon` to activate the environment

## Commands

All commands are run from the root directory of the project.

### aiohttp

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/aiohttp/ \
    --output-dir __internal__/collected_tests_hybrid/v1/aiohttp/ \
    --log-file __internal__/_logs/aiohttp_tests_analysis_output.txt
```

### connexion

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/connexion/ \
    --output-dir __internal__/collected_tests_hybrid/v1/connexion/ \
    --log-file __internal__/_logs/connexion_tests_analysis_output.txt
```

### django

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/django/ \
    --output-dir __internal__/collected_tests_hybrid/v1/django/ \
    --log-file __internal__/_logs/django_tests_analysis_output.txt
```

### fastapi

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/fastapi/ \
    --output-dir __internal__/collected_tests_hybrid/v1/fastapi/ \
    --log-file __internal__/_logs/fastapi_tests_analysis_output.txt
```

### flask

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/flask/ \
    --output-dir __internal__/collected_tests_hybrid/v1/flask/ \
    --log-file __internal__/_logs/flask_tests_analysis_output.txt
```

### gunicorn

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/gunicorn/ \
    --output-dir __internal__/collected_tests_hybrid/v1/gunicorn/ \
    --log-file __internal__/_logs/gunicorn_tests_analysis_output.txt
```

### pyramid

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/pyramid/ \
    --output-dir __internal__/collected_tests_hybrid/v1/pyramid/ \
    --log-file __internal__/_logs/pyramid_tests_analysis_output.txt
```

### sanic

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/sanic/ \
    --output-dir __internal__/collected_tests_hybrid/v1/sanic/ \
    --log-file __internal__/_logs/sanic_tests_analysis_output.txt
```

### starlette

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/starlette/ \
    --output-dir __internal__/collected_tests_hybrid/v1/starlette/ \
    --log-file __internal__/_logs/starlette_tests_analysis_output.txt
```

### tornado

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/tornado/ \
    --output-dir __internal__/collected_tests_hybrid/v1/tornado/ \
    --log-file __internal__/_logs/tornado_tests_analysis_output.txt
```

### uvicorn

```bash
python -m src.gluon.collect_tests.analyze_unit_tests \
    --input-dir __internal__/_data/uvicorn/ \
    --output-dir __internal__/collected_tests_hybrid/v1/uvicorn/ \
    --log-file __internal__/_logs/uvicorn_tests_analysis_output.txt
```
