from pathlib import Path
from typing import List

import seutil as su
from jsonargparse import CLI


def foo():
    """A simple (util) function that will be tested in the test file."""
    return 1 + 1


class EntryPoint:
    """
    This class serves as the entry point from the command line (by using jsonargparse).
    All the arguments of all functions in this class require type hints! (except for `self`).

    General command line format:
    ```
    python -m [fully qualified file name] [class-level args] [function] [function-level args]
    ```

    Examples for this file:
    ```
    python -m TODO_pkg_name.example_main --work_dir ./_work print --inputs=[1,2,3]
    python -m TODO_pkg_name.example_main print  # use default values
    ```

    You can also do `python -m TODO_pkg_name.example_main --help` to see the help message.
    """

    # All arguments specified in the __init__ function are class-level arguments
    def __init__(
        self,
        work_dir: su.arg.RPath = Path(__file__).parent.parent.parent / "_work",
        # su.arg.RPath: use this type hint for any path (relative or absolute) passed from command line.
        #   Do NOT use `Path` as the type hint.
        # You can specify default values of arguments in the function signature using `= value`;
        #   The default value here points to `/_work` directory under the root of the project.
    ):
        self.work_dir = work_dir

    def print(self, inputs: List[int] = None):
        # If the default value is a mutable data structure (like List), don't write in the function signature;
        #   write None in the functional signature and check for it at the beginning of the function instead.
        # Similar to List, there is also Dict, Tuple, Set, etc. that you can import from `typing`.
        if inputs is None:
            inputs = [0]

        print(f"work_dir: {self.work_dir}")
        print(f"inputs: {inputs}")
        print(f"The result of foo() is {foo()}")

    def read_args(self, f: float, i: int, s: str, strs: List[str]):
        # This lists some other typical types of arguments you can read from the command line.
        print(f"f: {f}")
        print(f"i: {i}")
        print(f"s: {s}")
        print(f"strs: {strs}")


if __name__ == "__main__":
    # Using jsonargparse.
    # The first argument is the entry point class; you can also pass a function instead.
    # as_positional=False forces the key-value format command line (`--key value` or `--key=value`), which
    #   I think is more clear; you can set as_positional=True (the default value) for simple command line arguments,
    #   which allows specifying only values (`value1 value2`) that will be processed according to their positions.
    CLI(EntryPoint, as_positional=False)
