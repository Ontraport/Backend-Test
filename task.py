inputDictionary = {'one': {'two': 3, 'four': [
    5, 6, 7], 'abc': [30, 36, 99]}, 'eight': {'nine': {'ten': 11}, 'def': 78, 'ghi': [23, 234, 563]}}


def multiDimensionalConverter(input):
    return multiDimensionalConverterRec(inputDictionary, {}, [])


def multiDimensionalConverterRec(input, output, path):
    for node in input:
        path.append(node)
        if (type(input[node]) is dict):
            multiDimensionalConverterRec(input[node], output, path)
            del path[-1]

        elif (type(input[node]) is list):
            inputList = input[node]
            for index in range(len(inputList)):
                output['/'.join(path)+'/'+str(index)] = inputList[index]
            del path[-1]

        elif (type(input[node]) is str or type(input[node]) is int):
            output['/'.join(path)] = input[node]
            del path[-1]

    return output


def singleDimensionalConverter(input):
    tempParent = {}
    output = {}
    tempParent = output
    for element in input:
        elementArray = element.split('/')
        for index in range(len(elementArray)):
            if (index == 0):
                if(elementArray[index] not in output):
                    output[elementArray[index]] = {}
                tempParent = output[elementArray[index]]
            elif (index == len(elementArray)-1):
                if(elementArray[index].isnumeric()):
                    tempParent.append(input[element])
                else:
                    tempParent[elementArray[index]] = input[element]
            else:
                if(elementArray[index] not in tempParent):
                    if (index == len(elementArray)-2) and (elementArray[-1].isnumeric()):
                        tempParent[elementArray[index]] = []
                    else:
                        tempParent[elementArray[index]] = {}
                tempParent = tempParent[elementArray[index]]

    return output


result = multiDimensionalConverter(inputDictionary)

revresult = singleDimensionalConverter(result)

print(result)
print(revresult)
