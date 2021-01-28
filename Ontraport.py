import json

separator = '/'

def flatten_json(json_object):
    flattened_json = {}

    def flatten(x, flattened_string=''):
        # if we have a json dictionary, flatten all its values
        if type(x) is dict:
            for value in x:
                flatten(x[value], flattened_string + value + separator)
        
        # if we have a list, separate the elements into "rows" and add the value's index in the list at the end
        elif type(x) is list:
            index = 0
            for value in x:
                flatten(value, flattened_string + str(index) + separator)
                index += 1

        # finaly...just values. store the row
        else:

            # remove last "/" and turn add the row to the output dictionary
            flattened_json[flattened_string[:-1]] = x

    flatten(json_object)

    return flattened_json

def unflatten_json(flattened_json):

    # return a dictionary containing the unflatted values
    output_dictionary = dict()

    for row_key in flattened_json:
        value = flattened_json[row_key]

        # split the line up into the component parts
        parts = row_key.split(separator)

        # if the last digit in the row is an index, then we have a list. remove the index and remember that we have an index for use a few lines down
        islist = False;
        if parts[-1].isdigit():
            islist = True;
            parts.pop()

        d = output_dictionary

        for part in parts[:-1]:
            # if the key isn't in the dictionary yet, add it
            if part not in d:
                d[part] = dict()
            d = d[part]

        # if we have a list, store all related rows in the list
        if islist:
            new_key = parts[-1]
            # if the list already exists, add the new element. otherwise, create the list and add it to the dictionary
            if new_key in d.keys():
                d[new_key].append(value)
            else:
                new_list = []
                new_list.append(value)
                d[new_key] = new_list

        # we have a non-list value, so add it to the dictionary
        else:
            d[parts[-1]] = value

    return output_dictionary


# test script
jsonString = '{ "one": { "two": 3, "four": [5, 6, 7] }, "eight": { "nine": {"ten": 11} } }'

jsonObject = json.loads(jsonString)
print("Original json: " + jsonString)

flattened = flatten_json(jsonObject)
print("Flattened json: " + str(flattened))

unflattened = unflatten_json(flattened)
print("Unflattened json: " + str(unflattened))
