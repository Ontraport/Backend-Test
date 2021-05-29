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


def compress(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        return compress_helper(data, {}, "")


def expand_helper(nodes, result, value, prev_node):
    for node in nodes:

        if node.isnumeric():
            if int(node) == 0:
                result[prev_node] = [value]
            else:
                result[prev_node].append(value)

        if node == nodes[-1]:
            result[node] = value

        elif node not in result.keys():
            result[node] = expand_helper(nodes[1:], {}, value, node)


def expand(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        result = {}
        for key in data:
            nodes = key.split('/')
            expand_helper(nodes, result, data[key], None)
    return result


# for every line:
#     for every node in line:
#         if key/node doesnt exist:
#             create key with value None
#             continue
#         if key/node does exist:
#             continue


def main():
    filename = sys.argv[1]
    file = open(filename, 'r')
    data = file.read()
    # print(compress(data))
    print(expand(data))


if __name__ == '__main__':
    main()
