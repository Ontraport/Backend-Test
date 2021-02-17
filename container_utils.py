"""
Author: Rohit Lunavara
Date: 02/16/2021
"""

SEPARATOR = "/"

def flatten(container):
    """
    Accepts a multi-dimensional container of any size and converts it into a one dimensional associative array whose keys are strings representing their value's path in the original container.

    E.g.

    Input:
    flatten([
        {
            "one": 1
        },
        {
            "two": {
                "three": 3
            }
        },
        {
            "four": [4, 5, {"five": [6]}]
        }
    ])

    Output:
    {
        "0/one": 1,
        "1/two/three": 3,
        "2/four/0": 4,
        "2/four/1": 5,
        "2/four/2/five/0": 6
    }
    """
    if len(container) == 0:
        return {}

    flattened_container = {}
    def recursive_flatten(container, current_key = None):
        # Default list argument results in shared list object between function calls, therefore, we initialize it separately
        if current_key is None:
            current_key = []

        if isinstance(container, dict):
            for key, value in container.items():
                recursive_flatten(value, current_key + [key])

        elif isinstance(container, list):
            for index, value in enumerate(container):
                recursive_flatten(value, current_key + [f"{index}"])

        else:
            string_key = SEPARATOR.join(current_key)
            flattened_container[string_key] = container

    recursive_flatten(container)
    return flattened_container

def widen(container):
    """
    Accepts a one dimensional associative array whose keys are strings representing their value's path in a multi-dimensional container and converts it into the original container based on the value's path.

    E.g.

    Input:
    widen({
        "0/one": 1,
        "1/two/three": 3,
        "2/four/0": 4,
        "2/four/1": 5,
        "2/four/2/five/0": 6
    })

    Output:
    [
        {
            "one": 1
        },
        {
            "two": {
                "three": 3
            }
        },
        {
            "four": [4, 5, {"five": [6]}]
        }
    ]
    """
    def recursive_replacement(container):
        """
        Recursively replaces dictionaries containing integer keys in string format with lists.
        Handles cases where there could be multiple nested dictionaries and lists.
        """
        if not isinstance(container, dict):
            return container

        any_random_key = next(iter(container))

        if isinstance(any_random_key, int):
            list_size = int(max(container)) + 1
            list_container = [None] * (list_size)

            for key, value in container.items():
                list_index = int(key)
                list_container[list_index] = recursive_replacement(value)

            return list_container

        else:
            for key, value in container.items():
                container[key] = recursive_replacement(value)

            return container

    if len(container) == 0:
        return container

    widened_container = {}
    # Store lists as dictionaries with integer keys, replace recursively later
    for key, value in container.items():
        current_keys = key.split(SEPARATOR)
        previous_container, current_container = None, widened_container

        for key in current_keys:
            modified_key = int(key) if key.isdigit() else key

            if modified_key not in current_container:
                current_container[modified_key] = {}

            previous_container, current_container = current_container, current_container[modified_key]

        previous_container[modified_key] = value

    return recursive_replacement(widened_container)

if __name__ == "__main__":
    # Test Cases
    widened_containers = [
        {
            "one": 1
        },
        {
            'one':
            {
                'two': 3,
                'four': [5, 6, 7]
            },
            'eight':
            {
                'nine':
                {
                    'ten': 11
                }
            }
        },
        [
            {
                "one": 1
            },
                {
                "two": {
                    "three": 3
                }
            },
            {
                "four": [4, 5, {"five": [6]}]
            }
        ],
    ]
    flattened_containers = [
        {
            "one": 1
        },
        {
            'one/two': 3,
            'one/four/0': 5,
            'one/four/1': 6,
            'one/four/2': 7,
            'eight/nine/ten': 11
        },
        {
            '0/one': 1,
            '1/two/three': 3,
            '2/four/0': 4,
            '2/four/1': 5,
            '2/four/2/five/0': 6
        },
    ]

    for index in range(len(widened_containers)):
        assert flatten(widened_containers[index]) == flattened_containers[index]
        assert widen(flattened_containers[index]) == widened_containers[index]

    assert flatten([]) == {}
    assert flatten({}) == {}
    assert widen([]) == []
    assert widen({}) == {}
