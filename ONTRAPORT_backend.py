


# go from a heirarchical key/value structure to a flat key/value where the heirarchy is encoded in the the syntax
def flatten_container(container, parent_key='', flattened=None):
    if flattened is None:
        flattened = {}
    
    # for every parent key, flatten the children
    if isinstance(container, dict):
        for key, value in container.items():
            new_key = f"{parent_key}/{key}" if parent_key else key
            flatten_container(value, new_key, flattened)
    
    # for every child, set the new keys
    elif isinstance(container, list):
        for index, value in enumerate(container):
            new_key = f"{parent_key}/{index}"
            flatten_container(value, new_key, flattened)

    # for every new parent key, set the value
    else:
        flattened[parent_key] = container
    
    return flattened

# use the flat encoding to separate the values and programatically create a structured dictionary
def unflatten_container(flattened_container):
    unflattened = {}

    # split the keys by the '/' separator
    for key, value in flattened_container.items():
        keys = key.split('/')
        current_dict = unflattened

        # for each key extracted from the line entry, create an empty dictionary entry
        for sub_key in keys[:-1]:
            if sub_key not in current_dict:
                current_dict[sub_key] = {}
            current_dict = current_dict[sub_key]

        last_key = keys[-1]

        # if it's the last key, append the value
        if isinstance(current_dict.get(last_key), list):
            current_dict[last_key].append(value)
        # otherwise, go throught the list and set the value
        elif isinstance(current_dict.get(last_key), dict):
            index = 0
            while f"{last_key}/{index}" in current_dict:
                index += 1
            current_dict[f"{last_key}/{index}"] = value
        else:
            current_dict[last_key] = value

    return unflattened