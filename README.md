# Template for Python-based AI+SE research project - TODO: replace it with your project name

Steps for using this template:

1. Replace `TODO_pkg_name` across the project to your package name (based on the project name)
  * Only lower case letters, numbers, and `_` (not recommended) are allowed in the package name; do NOT use other symbols
  * Prefer concise names and acronyms, e.g., `teco` instead of `test_completion`
  * Don't forget to rename the `src/TODO_pkg_name` directory

2. Check the build file `pyproject.toml` and replace as many `TODO_...` as possible

3. Test out your environment
  * Install [conda](https://docs.anaconda.com/miniconda/) if you haven't
  * Run `./prepare-env.sh` to create the conda environment
  * Run `conda activate TODO_pkg_name` to activate the environment
  * Run `python -m TODO_pkg_name.example_main --help` and see if the code runs (it should work from anywhere)
  * Run `pytest` to see the tests running (it must be run from the project root `/` or under `/tests`)
  * Run `conda deactivate` to exit the environment

4. Notes about bundled dependencies:

* `seutil` is a util library. There are some examples to use it in `example_main.py`.
  * In particular, `jsonargparse`, which is transitively installed by `seutil`, helps to parse command line arguments. Use it to read paths to inputs/outputs from command line, and avoid hardcoding them in code.
* `black` is a code formatter. Always format your Python code before committing.
  * Command line: `black .` (run from `/`)
  * VS Code: install `ms-python.black-formatter` plugin; then use `Format Document` command (`Ctrl+Shift+I` hotkey for me) & `Organize Imports` command (`Ctrl+Shift+O` hotkey for me) to format the code
* `ruff` is a code linter. Run it periodically to improve your code quality.
  * Command line: `ruff check .` (run from `/`)
  * VS Code: install `charliermarsh.ruff` plugin; suggestions should show up in the editor

5. Start developing your code
  * Replace the example code and this readme with your code/tests/documentation
  * If you have installed new dependencies using `pip install`, don't forget to add them to `pyproject.toml`
  * Write [type hints](https://docs.python.org/3/library/typing.html)
  * Write comments and docstrings
