# Elliot Brainerd
# Ontraport Backend Test 5/29

# usage:
# update main method according to input file format
# run python .\ontraport_test.py <filename>

# eg. 
# uncomment line in main "print(expand(data))"
# python ./ontraport_test.py input2.txt

# solution assumes that list values are final/do not contain nested data structures

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

        # integers
        else:
            result[cur_path + key] = data[key]

    return result


# accepts a multi-dimensional container of any size and converts it into a
# one dimensional associative array whose keys are strings representing
# their value's path in the original container
def compress(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        return compress_helper(data, {}, "")
    else:
        print("Error with input file.")
        exit


def expand_helper(nodes, result, value, prev_node):
    cur_node = nodes[0]  # nodes represent the keys in a given path

    # integer nodes
    if cur_node.isnumeric():
        result[prev_node].insert(int(cur_node), value)

    # last node, non-numeric
    elif cur_node == nodes[-1]:
        result[cur_node] = value

    # new node
    elif cur_node not in result.keys():
        if nodes[nodes.index(cur_node) + 1].isnumeric():
            result[cur_node] = [value]
        else:
            result[cur_node] = expand_helper(nodes[1:], {}, value, cur_node)

    # node already seen
    else:
        if type(result[cur_node]) == list:
            result[cur_node].insert(
                int(nodes[nodes.index(cur_node) + 1]), value)
        else:
            expand_helper(nodes[1:], result[cur_node], value, cur_node)

    return result


# accepts one dimensional associative array whose keys are strings representing
# their value's path and creates a multi-dimensional container
def expand(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        result = {}
        for key in data:
            nodes = key.split('/')
            expand_helper(nodes, result, data[key], None)
        return result
    else:
        print("Error with input file.")
        exit


def main():
    filename = sys.argv[1]
    file = open(filename, 'r')
    data = file.read()

    # input1.txt
    # print(compress(data))

    # input2.txt
    print(expand(data))


if __name__ == '__main__':
    main()
