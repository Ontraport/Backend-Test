#!/usr/bin/env python


def convert_to_associative(multidim, associative, _path=None):
    """
    :param multidim: a multi-dimensional container of any size.
    :param associative: an associative array (Python dict) to be populated by this function.
    :param _path: Internal variable, used to store the path to a associative array value.

    # Doctest
    >>> container = {'one': {'two': 3, 'four': [ 5,6,7]}, 'eight': {'nine': {'ten': 11}}}
    >>> associative = dict()
    >>> convert_to_associative(container, associative)
    >>> unm = set(associative.items()) ^ {('one/two', 3), ('one/four/0', 5), ('one/four/1', 6), ('one/four/2', 7), \
    ('eight/nine/ten', 11)}
    >>> len(unm) == 0
    True
    """

    if isinstance(multidim, dict):
        for key in multidim.keys():
            item = multidim.get(key)
            convert_to_associative(item, associative, "{}/{}".format(_path, key)) if _path is not None else \
                convert_to_associative(item, associative, key)
    elif isinstance(multidim, list):
        for index in range(len(multidim)):
            item = multidim[index]
            convert_to_associative(item, associative, "{}/{}".format(_path, index)) if _path is not None else \
                convert_to_associative(item, associative, "{}".format(index))
    else:
        associative[_path] = multidim


def revert_from_associative(associative, multidim):
    """
    :param associative: an one dimensional associate array (Python dict) representing a multi-dimensional container.
    :param multidim: a python dict to be populated by this function.

     #Doctest
     >>> associative = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine/ten': 11}
     >>> container = dict()
     >>> revert_from_associative(associative, container)
    """
    def populate_tree(container, path):
        if '/' not in path[0]:
            return path[1]

        next_slash = path.index('/')
        currentKey = path[:next_slash]

        if currentKey.isdecimal():
            if isinstance(container, list):
                container.insert(int(currentKey), populate_tree(path[next_slash+1:]))
            else:
                return [].insert(int(currentKey), populate_tree(path[next_slash+1:]))

    for path in associative.items():
        populate_tree(multidim, path)


    pass


if __name__ != "__main__":
    import doctest
    doctest.testmod()
