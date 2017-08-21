"""Tests for the Flatten application."""

import ast
import os

from flatten import flatten


PATH_PREFIX_FOR_TEST_DATA = os.path.join(os.path.dirname(__file__), "test_files")


def read_ast_from_test_file(filename):
    """Read and return an object from a filename."""
    with open(os.path.join(PATH_PREFIX_FOR_TEST_DATA, filename)) as file:
        return ast.literal_eval(file.read())


def test_contains_non_empty_int_range():
    """Test the 'flatten._contains_non_empty_int_range(...)' function."""
    assert not flatten._contains_non_empty_int_range({"1", "2"})
    assert not flatten._contains_non_empty_int_range({"1", "1", "3"})
    assert not flatten._contains_non_empty_int_range({"0", "1", "3"})
    assert not flatten._contains_non_empty_int_range(())
    assert not flatten._contains_non_empty_int_range(["-1", "0"])
    assert not flatten._contains_non_empty_int_range(["0", "1", "a"])
    assert flatten._contains_non_empty_int_range(("0", "1", "2", "0"))


def flatten_and_expand_files(file_to_flatten, file_to_expand):
    """Test whether or not 'file_to_flatten' flattens to 'file_to_expand' and vice versa."""
    data_to_flatten = read_ast_from_test_file(os.path.join(file_to_flatten))
    data_to_expand = read_ast_from_test_file(os.path.join(file_to_expand))
    return flatten.flatten(data_to_flatten) == data_to_expand and flatten.expand(data_to_expand) == data_to_flatten


def test_flatten_supplied_input():
    """Test flattening and expanding of the given sample data."""
    assert flatten_and_expand_files("supplied_input_expanded.txt", "supplied_input_flattened.txt")


def test_flatten_different_path_same_key():
    """Test to make sure that paths that have a key with the same name after diverging work well.

    An example would be 'x/y/z' and 'a/y/c'.
    """
    assert flatten_and_expand_files(
        "different_path_same_key_expanded.txt", "different_path_same_key_flattened.txt")


def test_flatten_outer_list():
    """Test a multidimensional container where the outermost item is a list."""
    assert flatten_and_expand_files("outer_list_expanded.txt", "outer_list_flattened.txt")


def test_flatten_single_list_element():
    """Make sure flattening/expanding a list with a single element works well."""
    assert flatten_and_expand_files("single_list_element_expanded.txt", "single_list_element_flattened.txt")


def test_main_with_supplied_input(capsys):
    """Test the main function. Make sure passing the options dictionary works well."""
    argv = {"--expand": False, "--flatten": True,
            "FILE": os.path.join(PATH_PREFIX_FOR_TEST_DATA, "supplied_input_expanded.txt")}
    correct_output = read_ast_from_test_file(os.path.join("supplied_input_flattened.txt"))
    flatten.main(argv)
    output, _ = capsys.readouterr()
    assert ast.literal_eval(output) == correct_output

    argv = {"--expand": True, "--flatten": False,
            "FILE": os.path.join(PATH_PREFIX_FOR_TEST_DATA, "supplied_input_flattened.txt")}
    correct_output = read_ast_from_test_file(os.path.join("supplied_input_expanded.txt"))
    flatten.main(argv)
    output, _ = capsys.readouterr()
    assert ast.literal_eval(output) == correct_output


def test_expand_empty():
    """Trying to expand an empty dictionary should result in an absence of data indicated by 'None'."""
    assert flatten.expand({}) is None


def test_flatten_empty():
    """Trying to flatten an empty container should return an empty dictionary."""
    assert flatten.flatten([]) == {}
    assert flatten.flatten({}) == {}
