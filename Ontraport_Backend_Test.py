def recurse_container(container, str_k='', associative_array={}):
    """
    Recursive function that accepts a nested dictionary of any size and converts it into a one dimensional
    associative dictionary whose keys are strings representing their value's path in the original container

    Parameters:
        container (dict): a dictionary containing str type keys and either dict, int, or list type values
        str_k (str): str type key path that will be built recursively as the dictionary is traversed
        associative_array (dict): one dimensional dictionary representing the original container nested dictionary

    Return:
        associative_array (dict): one dimensional dictionary representing the original container nested dictionary
    """
    # Handle potential user errors, can modify depending on intended function use
    if not container:
        raise ValueError("Container is empty.")
    elif not isinstance(container, (dict, int, list)) or not type(str_k) == str:
        raise TypeError("Invalid type found in container. Only supports 'str' keys "
                        "and 'dict', 'int', or 'list' values.")
    # Traverse dictionary down to leaf node
    if isinstance(container, dict):
        for k, v in container.items():
            next_str_k = str_k + '/' + k if str_k else k
            recurse_container(v, next_str_k, associative_array)
    # Add str_k path key and int value to 1D associative array
    else:
        if isinstance(container, int):
            associative_array[str_k] = container
        elif isinstance(container, list):
            for idx, val in enumerate(container):
                associative_array[f'{str_k}/{idx}'] = val
    return associative_array


def nested_container(flat_container, nest_container={}):
    """
    Iterative function that accepts a flat 1D dictionary and converts it into a nested dictionary.
    Flat dictionary is of any size, its keys are paths for a nested dictionary and
    values are the value at the end of each key path.

    Parameters:
        flat_container (dict): a dictionary containing string keys and integer values
        nest_container (dict): empty dictionary that will become the nested dictionary defined by the one dimensional
        associative container

    Return:
        nest_container (dict): nested dictionary representing the original one dimensional associative container
    """
    # Handle potential user errors, can be modified depending on intended function use
    for k, v in flat_container.items():
        if type(k) != str and type(v) != int:
            raise TypeError("Invalid type in container. Keys must be strings and values must be integers.")
    # Iterate each key, value pair in associative container
    for key, value in flat_container.items():
        current = nest_container
        keys = key.split('/')
        # If last key in path does not indicate a list value at branch end, nest each key and append value with last key
        if not keys[-1].isdigit():
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
        # If last key indicates list value type at branch end, nest each key until second to last key, use last key as
        # list index to insert value to appropriate list index
        elif keys[-1].isdigit():
            for k in keys[:-1]:
                if k != keys[-2]:
                    current = current.setdefault(k, {})
                else:
                    current = current.setdefault(k, [])
            current.insert(int(keys[-1]), value)
    return nest_container


def test_recurse_container():
    test_dict = {'one': {'two': 3, 'four': [5, 6, 7]}, 'eight': {'nine': {'ten': 11}}}
    assoc_dict = recurse_container(test_dict)
    expected_output = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine/ten': 11}
    assert assoc_dict == expected_output


def test_nested_container():
    test_dict = {'one': {'two': 3, 'four': [5, 6, 7]}, 'eight': {'nine': {'ten': 11}}}
    flat_container = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine/ten': 11}
    renested_dict = nested_container(flat_container)
    assert renested_dict == test_dict


if __name__ == '__main__':
    test_recurse_container()
    test_nested_container()
