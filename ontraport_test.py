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


def expand_helper(result, cur_path_list):
    top = cur_path_list.pop(0)
    if top not in result.keys() and not top.isnumeric():
        result[top] = expand_helper({}, cur_path_list)
    elif top in result.keys():
        expand_helper(result[top], cur_path_list[1:])
    elif top.isnumeric():
        pass


def expand(data):
    data = ast.literal_eval(data)
    if type(data) is dict:
        result = {}
        for key in data:
            spl = key.split("/")
            expand_helper(result, spl)
        return result


for every line:
    for every node in line:
        if key/node doesnt exist:
            create key with value None
            continue
        if key/node does exist:
            continue


def main():
    filename = sys.argv[1]
    file = open(filename, 'r')
    data = file.read()
    # print(compress(data))
    expand(data)


if __name__ == '__main__':
    main()
