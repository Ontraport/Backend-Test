import json

data = { 'one': { 'two': 3, 'four': [ 5,6,7] }, 'eight': { 'nine': { 'ten':11 } }, 'eleven': 12, 'twelve': [1,3,5] }

def dToString(data):
    '''
    Answer to Question 1
    Takes in multi-dimensional data and returns a single dimension array
    '''
    d = {}
    dfsDtoString(data, d, [])
    return d

def dfsDtoString(data, d, currentPath):
    for key, value in data.items():
        currentPath.append(key)
        if isinstance(value, int) or isinstance(value, str) or isinstance(value, float):
            d['/'.join(currentPath)] = value
        elif isinstance(value, list):
            for i in range(len(value)):
                d['/'.join(currentPath) + '/' + str(i)] = value[i]
        elif isinstance(value, dict):
            dfsDtoString(value, d, currentPath)
        del currentPath[-1]


data2 = {'one/two': 3, 'one/four/0': 5, 'one/four/1': 6, 'one/four/2': 7, 'eight/nine/ten': 11, 'eleven': 12, 'twelve/1': 3, 'twelve/0': 1, 'twelve/2': 5, 'twelve/6': 7}

def stringToD(data):
    '''
    Answer to Question 2
    Takes in single dimension array and returns a multi-dimensional array
    '''

    d = {}

    for key, value in data.items():
        nodes = key.split('/')

        if len(nodes) == 1:
            d[nodes[-1]] = value
            continue

        t = d

        flag = False
        if nodes[-1].isnumeric():
            flag = True
            
        for i in range(len(nodes)-1):
            if nodes[i] not in t:
                if flag and i == len(nodes)-2:
                    t[nodes[i]] = []
                else:
                    t[nodes[i]] = {}
            t = t[nodes[i]]
            
        if flag:
            pos = int(nodes[-1])
            if 0 <= pos < len(t):
                t[pos] = value
            else:
                for i in range(len(t), pos+1):
                    t.append(None)
                t[pos] = value
        else:
            t[nodes[-1]] = value

    return d




# Question 1
print(dToString(data))
# Question 2
print(stringToD(data2))