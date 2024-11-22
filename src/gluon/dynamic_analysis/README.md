# Dynamic Analysis

To perform dynamic analysis, we need to set up the environment to run the code of the target program. It is better to use built-in Python libraries to avoid the conflicts with the libraries of the target program.

Built-in Python libraries that are helpful for dynamic analysis can be found in [Python Standard Library](https://docs.python.org/3/library/).

## Set up

1. Clone the repository
2. Build hooks with the built-in Python libraries
3. Run the target program with the hooks

## Hooks

Hooks are the functionalities that are injected into the target program to perform dynamic analysis. There are many examples for this.

- Print the stack trace
- Print the variable values
- Print the run time of the function
- etc.

## Repos

[Flask](https://github.com/pallets/flask)

```bash
git clone https://github.com/pallets/flask.git
cd flask
pip install -e ".[dev]"
# Run all tests
pytest -v
# Show all test cases
pytest --collect-only -v
```
