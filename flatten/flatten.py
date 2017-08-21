#!/usr/bin/env python3

"""Flatten: a tool for flattening (and expanding) multidimensional lists and dictionaries.

Usage:
  flatten.py (-e | -f) FILE
  flatten.py (-h | --help)
  flatten.py (-v | --version)

Options:
  -e --expand   Expand a file. Read from standard input if "-" is supplied as the file name.
  -f --flatten  Flatten a file. Read from standard input if "-" is supplied as the file name.
  -h --help     Show this screen.
  -v --version  Show version.

"""

import ast
import itertools
import pprint
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

import docopt


def main(argv: Dict[str, Any]) -> None:
    """Read a data file, and print its "flattened" or "expanded" version."""
    if argv["FILE"] == "-":
        data_file_read = sys.stdin.read()
    else:
        with open(argv["FILE"]) as data_file:
            data_file_read = data_file.read()

    data = ast.literal_eval(data_file_read) if data_file_read else None

    output: Optional[Union[Dict, List]]
    if argv["--flatten"]:
        output = flatten(data)
    elif argv["--expand"]:
        output = expand(data)
    else:
        sys.exit("Couldn't parse an action to run. Read the help section and try again. Exiting.")

    pprint.pprint(output)


def flatten(data: Union[Dict, List]) -> Dict[str, Any]:
    """Return the "flattened" version of a dictionary or list."""
    if not data:
        return {}

    output: Dict[str, Any] = {}

    # first element of tuple is the dictionary to process and second element is the path taken through the keys to get
    # to that sub-dictionary. The path is represented as a string in which separate keys are separated by "/"
    stack = [(data, "")]
    while stack:
        current_data, current_path = stack.pop()
        if isinstance(current_data, dict):
            # go through each k/v pair in the dictionary we're currently processing
            for key, value in current_data.items():
                # value is another dict. add its key to the path and add the value/new path pair
                # to the stack for processing
                stack.append((value, f"{current_path}/{key}"))
        elif isinstance(current_data, list):
            # value is a list, add each list item with its corresponding index as the end of the
            # output key to the output
            for index, value in enumerate(current_data):
                stack.append((value, f"{current_path}/{index}"))
        else:
            # for all other types of objects, we simply add them to the output with the key being the current path
            # without the leading slash
            output[current_path[1:]] = current_data

    return output


def expand(data: Dict[str, Any]) -> Optional[Union[Dict, List]]:
    """Return the "expanded" version of a dictionary."""
    if not data:
        return None

    # determine if the outermost structure is a list or dictionary. a list is only used in the overall data structure
    # if its child keys form a continuous integer range 0..N
    outermost_keys_unique = {i.partition("/")[0] for i in data.keys()}
    output: Union[Dict, List]
    if _contains_non_empty_int_range(outermost_keys_unique):
        output = [None] * len(outermost_keys_unique)
    else:
        output = {}

    runs_to_process = [_RunState(k.split("/"), output, v) for k, v in data.items()]
    # perform a breadth-first traversal of all the paths of the tree (keys in the passed in dict) to populate the tree.
    # each cycle of this loop processes one layer of depth in the paths (so one key in all remaining paths)
    while runs_to_process:
        # group all runs by their current position in the tree (they're all at the same depth)
        run_keys_and_groups = itertools.groupby(sorted(runs_to_process, key=_RunState.get_tree_position_identifier),
                                                key=_RunState.get_tree_position_identifier)
        runs_to_process.clear()

        for _, group in run_keys_and_groups:
            runs_at_same_position_in_tree = list(group)  # runs with a common current position in the tree

            # the current item should be a list only if its immediate child keys are all integers that form a continuous
            # integer range from 0 to some positive number. repeat keys are fine.
            next_keys_unique = {run.rest_of_path[0] for run in runs_at_same_position_in_tree if run.rest_of_path}
            new_insertion_point: Union[Dict, List]
            if _contains_non_empty_int_range(next_keys_unique):
                new_insertion_point = [None] * len(next_keys_unique)
            else:
                new_insertion_point = {}

            for run in runs_at_same_position_in_tree:
                # if the end of the run has been reached, add the run's final value to the current insertion point.
                # otherwise, add the current key/new_insertion_point pair to the current insertion point
                item_to_add = run.value if not run.rest_of_path else new_insertion_point
                if isinstance(run.insertion_point, list):
                    run.insertion_point[int(run.current_key)] = item_to_add
                else:
                    run.insertion_point[run.current_key] = item_to_add
                if run.rest_of_path:
                    # add the remainder of the run (if there is one) to the list of runs to be processed
                    runs_to_process.append(_RunState(run.rest_of_path, new_insertion_point, run.value))

    return output


class _RunState:
    """The state of a "run" down the tree following a single key/path in the dictionary argument to "expand(...)".

    A "run" is the remaining path (keys) down the tree to take, the container to insert the next key into, and the
    final value.
    """

    def __init__(self, path: List[str], insertion_point: Union[Dict, List], value: Any) -> None:
        self.path = path
        self.insertion_point = insertion_point
        self.value = value

        self.current_key, *self.rest_of_path = path

    @staticmethod
    def get_tree_position_identifier(run: '_RunState') -> Tuple[int, str]:
        """Return an identifier that uniquely determines this run's current position in the tree. Used for grouping.

        The current position is just this run's path down the tree up to and including the current key. The id of the
        insertion point uniquely determines the path up to but not including the current key.
        """
        return id(run.insertion_point), run.current_key


def _contains_non_empty_int_range(iter_: Iterable) -> bool:
    """Return True iff the iterable isn't empty and contains each element of "range(len(set(iter_)))" at least once."""
    if not iter_:
        return False

    try:
        set_ = {int(i) for i in iter_}
    except ValueError:
        return False
    return set_ == set(range(len(set_)))


if __name__ == "__main__":
    main(docopt.docopt(__doc__, version="1.0"))
