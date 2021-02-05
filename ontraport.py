"""
ontraport.py
By: Irvin Leshchinsky | 2/4/2021
Compatibility: Python 3.8.5 
(In order to ensure correct function please use v 3.8.5 or higher)

Collection of functions set to solve Problems 1 and 2 as defined
in https://github.com/Ontraport/Backend-Test.

Usage:
- multi_to_single(multi_container) solves Problem 1
- single_to_multi(single_container) solves Problem 2

"""

from collections import deque

def deep_merge(dict1: dict, dict2: dict) -> dict:
    """
    Function takes in two dictionaries and merges them into into first dict,
    combining sub-dictionaries and sub-lists into the same key instead of overwriting them
    like update() does. In cases where the value is not a dict or list, function acts like update()

    Args: 
        dict1 (dict): A primary dictionary you want to merge another dictionary in to
        dict2 (dict): A secondary dictionary that you want to merge into the previous
    Returns:
        A merged dictionary that contains the merged values from dict1 and dict2
    
    """
    q = deque([(dict1, dict2)])
    while len(q) > 0:
        d1, d2 = q.pop()
        for k, v in d2.items():
            if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
                q.append((d1[k], v))
            elif k in d1 and isinstance(d1[k], list) and isinstance(v, list):
                d1[k] = d1[k] + v
            else:
                d1[k] = v
    return dict1

def multi_to_single(multi_container: dict) -> dict:
    """
    Function takes in a dictionary of any dimension or size and compresses it,
    creating a one-dimensional dictionary whose keys are string representing a
    path that indicates the original structure of the dictionary

    Args:
        multi_container (dict): A dictionary of any dimension or size with string keys
    Returns:
        A single-dimensional dictionary
    
    """
    return multi_to_single_rec(multi_container, "")

def multi_to_single_rec(inner_container: dict, built_key: str) -> dict:
    """
    Recursive helper function of multi_to_single(). Recurses down a dictionary branch
    and builds a singular key/value dictionary that is eventually merged to {final}.

    Args:
        inner_container (dict): A dictionary of any dimension or size with string keys
        built_key (str): A string consisting of the path traversed down a dictionary branch
    Returns:
        A single-dimensional dictionary

    """
    final = {}
    for item in inner_container.items():
        key, value = item
        if (isinstance(value, dict)):
            final.update(multi_to_single_rec(value, built_key + str(key) + '/'))
        elif (isinstance(value, list)):
            built_key = built_key + str(key) + '/'
            for list_index, list_val in zip(list(range(0,len(value))),value):
                final[built_key + str(list_index)] = list_val
        else:
            final[built_key + str(key)] = value
    return final

def single_to_multi(single_container: dict) -> dict:
    """
    Function takes in a single-dimensional dictionary and expands it to a multi-dimensional dictionary,
    whose structure is based on the path represented in each key. For condensed [list] values, the function
    assumes the order of the key/pairs to reflect their relative place in the [list], 
    matching the condensing order of multi_to_single().

    Args:
        single_container (dict): A single-dimensional dictionary
    Returns:
        An multi-dimensional dictionary that is the expanded form of the initial dictionary
    
    """
    final = {}
    for key, value in single_container.items():
        current = {}
        split_keys = str(key).split('/')
        temp_list = None
        for cur_key in split_keys[::-1]:    # We are going backwards to get the base key/val pair
            if len(current) == 0:
                if (cur_key.isnumeric()):   # If we reach a list item, convert the value to a [list]
                    value = [value]
                else:
                    current[cur_key] = value
            else:
                temp = current
                current = {}
                current[cur_key] = temp
        deep_merge(final,current)
    return final

def main():
    multi_container = {
        'one':
        {
            'two': 3,
            'four': [5,6,7]
        },
        'eight':
        {
            'nine':
            {
                'ten':11
            }
        }
    }

    single_container = {
    'one/two':3,
    'one/four/0':5,
    'one/four/1':6,
    'one/four/2':7,
    'eight/nine/ten':11
    }

    # Simple test based off of prompt
    print(multi_to_single(multi_container))
    print(single_to_multi(single_container))

if __name__ == "__main__":
    main()
