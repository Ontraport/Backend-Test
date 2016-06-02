

# Coded with Python 3.4


import sys
assert sys.version_info >= (3,0)



INPUT_DICTIONARY = {
    'one/two':3,
    'one/four/0':5,
    'one/four/1':6,
    'one/four/2':7,
    'eight/nine/ten':11
}




import re
import pprint






def _getEmptyContainer(containerStr):
    if re.search('^[0-9]+$', containerStr):
        return list()
    return dict()



def _getUsableIndex(containerStr):
    if re.search('^[0-9]+$', containerStr):
        return int(containerStr)
    return containerStr




def _doesElementExistAtIndex(index, container):
    try:
        x = container[index]
        if x == None:
            return False
    except (KeyError, IndexError, TypeError):
        return False
    return True


def _setElement(index, container, element):
    '''
    Lists have indices starting at 0 and are consecutive -- holes are filled in with None.
    '''
    if isinstance(container, dict):
        container[index] = element
    elif isinstance(container, list):
        if index < 0:
            raise IndexError('Index out of bounds')
        while len(container) <= index:
            container.append(None)
        container[index] = element

    else:
        raise TypeError('Container type not supported: ' + str(type(container)))




def convertToMultiDAry(dictionary):
    '''
    Converts a dictionary (associative array) into a multi-dimensional array as specified on the GitHub page.
    The keys are split on '/'. Any resulting empty strings,including leading/trailing and between side-by-side slashes ('//'),
    are kept as valid keys into the multi-dimensional array.
    The resulting multi-dimensional array will be made up of dictionaries and lists.
    The delimited strings in the original input keys are taken to denote lists if they are integer literals,
    and dictionaries otherwise. An exception will be raised for trying to use both dictionaries and lists at the same spot
    in the multi-dimensional array.
    Lists in the output array have indices starting at 0 and are consecutive -- holes are filled in with None.
    Trying to overwrite parts of the output array with new sequences/values will result in exceptions.
    References to the values of the original dictionary are put into the resulting multi-dimensional array as-is.
    The dictionary parameter itself will not be modified.
    '''

    if not dictionary:
        return None


    mDAry = None
    curContainer = None


    for keyOrig in dictionary.keys():

        chain = keyOrig.split('/')
        chain.append(dictionary[keyOrig])



        valueIndex = len(chain)-1

        if mDAry == None:
            mDAry = _getEmptyContainer(chain[0])
            curContainer = mDAry

        for chainElementIndex in range(0, valueIndex):

            chainElement = chain[chainElementIndex]
            usableIndex = _getUsableIndex(chainElement)

            if type(curContainer) != type(_getEmptyContainer(chainElement)):
                raise Exception('Tried to overwrite a part of the multi-dimensional array with a new type: ' + str(chain))

            if chainElementIndex+1 == valueIndex:
                if _doesElementExistAtIndex(usableIndex, curContainer):
                    raise Exception('Tried to set a value in the multi-dimensional array at a spot that was already occupied: ' + str(chain))
                _setElement(usableIndex, curContainer, chain[valueIndex])
            else:
                if not _doesElementExistAtIndex(usableIndex, curContainer):
                    _setElement(usableIndex, curContainer, _getEmptyContainer(chain[chainElementIndex+1]))
                curContainer = curContainer[usableIndex]

        curContainer = mDAry


    return mDAry






mDAry = convertToMultiDAry(INPUT_DICTIONARY)
printer = pprint.PrettyPrinter(width=-1)
printer.pprint(mDAry)