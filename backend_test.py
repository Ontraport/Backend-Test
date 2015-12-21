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


def revert_from_associative(associative):
    """
    :param associative: an one dimensional associate array (Python dict) representing a multi-dimensional container.

     #Doctest
     >>> associative = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine/ten': 11}
     >>> print(revert_from_associative(associative).__eq__({'one': {'two': 3, 'four': [5, 6, 7]}, 'eight':\
      {'nine': {'ten': 11}}}))
     True
    """

    def populate_tree(item, container=None):
        try:
            next_slash = item[0].index('/')
            current_key = item[0][:next_slash]
            item[0] = item[0][next_slash + 1:]

            if not (current_key).isnumeric():
                if container is None:
                    container = {}

                if current_key not in container:
                    container[current_key] = populate_tree(item, None)
                else:
                    populate_tree(item, container[current_key])
            else:
                if container is None:
                    container = []

                if len(container) < int(current_key) + 1:
                    container.append(populate_tree(item, None))
                else:
                    populate_tree(item, container[int(current_key)])
        except ValueError:
            if not item[0].isnumeric():
                if container is None:
                    container = {}
                container[item[0]] = item[1]
            else:
                if container is None:
                    container = []
                container.append(item[1])

        return container

    from operator import itemgetter

    items_tuple = sorted(associative.items(), key=itemgetter(0))
    multidim = populate_tree(list(items_tuple[0]))

    for item in items_tuple[1:]:
        populate_tree(list(item), multidim)

    return multidim

if __name__ != "__main__":
    import doctest
    doctest.testmod()
