# Elliot Brainerd
# Ontraport Backend Test 5/29

# Usage: python .\ontraport_test.py <filename>

import sys
import ast


def compress_helper(data, result, cur_path):
    for key in data:

        if type(data[key]) is dict:
            cur_path += key + "/"
            compress_helper(data[key], result, cur_path)
            cur_path = ""

        elif type(data[key]) is list:
            cur_path += key + "/"
            cur_path_copy = cur_path
            for i in range(len(data[key])):
                cur_path_copy += str(i)
                result[cur_path_copy] = data[key][i]
                cur_path_copy = cur_path

        else:
            result[cur_path + key] = data[key]

    return result


# Accepts a multi-dimensional container of any size and converts it into a
# one dimensional associative array whose keys are strings representing
# their value's path in the original container
def compress(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        return compress_helper(data, {}, "")


def expand_helper(nodes, result, value, prev_node):
    node = nodes[0]

    # integer nodes (for lists)
    if node.isnumeric():
        if type(result[prev_node] != list):
            result[prev_node] = []
        result[prev_node].insert(int(node), value)

    # last node, non-numeric
    elif node == nodes[-1]:
        result[node] = value

    # new node, new dict
    elif node not in result.keys():
        if nodes[nodes.index(node) + 1].isnumeric():
            result[node] = [value]
        else:
            result[node] = expand_helper(nodes[1:], {}, value, node)

    # node already seen
    else:
        if type(result[node]) == list:
            result[node].append(value)
        else:
            expand_helper(nodes[1:], result[node], value, node)

    return result


# Accepts one dimensional associative array whose keys are strings representing
# their value's path and creates a multi-dimensional container
def expand(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        result = {}
        for key in data:
            nodes = key.split('/')
            expand_helper(nodes, result, data[key], None)
    return result


def main():
    filename = sys.argv[1]
    file = open(filename, 'r')
    data = file.read()
    # compressed = compress(data)
    # expanded = expand(data)


if __name__ == '__main__':
    main()
