
# Coded with Python 3.4



import sys
assert sys.version_info >= (3,0)




INPUT_CONTAINER = {
    'one':
    {
        'two': 3,
        'four': [ 5,6,7]
    },
    'eight':
    {
        'nine':
        {
            'ten':11
        }
    }
}




import pprint




def _isContainer(obj):
    if isinstance(obj, dict):
        return True
    if isinstance(obj, list):
        return True
    return False




def _getIndices(container):

    if isinstance(container, dict):
        return list(container.keys())
    if isinstance(container, list):
        return list(range(0, len(container)))
    raise TypeError('Container type not supported: ' + str(type(container)))




def _convertToDictRecur(container, pathSoFar, outputDict):

    for index in _getIndices(container):
        obj = container[index]
        if pathSoFar:
            newPath = pathSoFar + '/' + str(index)
        else:
            newPath = str(index)
        if _isContainer(obj):
            _convertToDictRecur(obj, newPath, outputDict)
        else:
            outputDict[newPath] = obj





def convertToDict(container):
    '''
    Converts container to a dictionary (associative array) as described on the GitHub page.
    Types list and dictionary are considered containers; everything else is considered a value.
    The result is returned; the original container is not modified.
    Caveats: 1) Values with duplicate paths
    (such as could happen when there is both a string key 'i' and integer key i for any given container)
    get overwritten.
    2) Empty strings and forward slashes in input keys are not treated specially.
    '''

    outputDict = dict()
    _convertToDictRecur(container, '', outputDict)
    return outputDict






output = convertToDict(INPUT_CONTAINER)
printer = pprint.PrettyPrinter(width=-1)
printer.pprint(output)