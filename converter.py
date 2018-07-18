import json
import re
import os
import os.path

'''
    Contains functions that can be used to flatten and unflatten json data.

    Upon running the main method, the file "./test.json" will be read into a dictionary, assuming that it exists.
    The original data from the file is printed, then the results from flatten() are printed, and then
    the results from flatten() are passed to unflatten(), and the results of which are also printed.
'''

def flatten(oldData, newData=None, parentKey='', delim='/', width=1):
    '''
    Takes a dictionary containing JSON data of any dimension, and flattens
    it to a single dimension.
    
    Parameters:
    oldData (dict/list): json collection of any dimension to be flattened. In a recursive
        case, oldData can be used to contain an a list of json values
    newData (dict): dict containing the flattened json.
    parentKey (str): Represents the flattened key in the form of a path
    delim (str): Delimitter used for separating keys
    width (int): Minimum digits used to represent indices for list values. Does not need
        to be adjusted for larger lists

    Returns:
    dict: Dictionary containing data from oldData compressed into single dimension
    '''
    # If function is just starting
    if newData is None:
        newData = {}
    # If oldData is a list, recursive case
    if isinstance(oldData, list):
        # If the list has size of 1, simply append "/0" to parentKey and pass
        # it to recursive call along with the list value
        if len(oldData) == 1:
            flatten(oldData[0], newData, parentKey + "/0")
        else:
            # For every element in oldData, create newKey
            # from parentKey (path of keys) and i (index for list)
            # and then make recursive call with the current list value
            for i, elem in enumerate(oldData):
                newKey = "{}{}{:0>{}}".format(parentKey, delim if parentKey else '', i, width)
                flatten(elem, newData, newKey)
    # If oldData is a dictionary, recursive case
    elif isinstance(oldData, dict):
        for k, v in oldData.items():
            # Add the current key onto the parentKey
            # If parentKey is empty, set newKey to k
            newKey = parentKey + delim + k if parentKey else k
            flatten(v, newData, newKey)
    # Base case
    else:
        # Add parentKey to the dictionary if it hasn't been added yet
        if parentKey not in newData:
            newData[parentKey] = oldData
            
    return newData


def printFlattenedJSON(flattenedJSON):
    '''
    Takes a dictionary of flattened json, formats it, and prints it

    Parameters:
    flattenedJSON (dict): dictionary containing flattened json data
    '''
    #Takes a dictionary of flattened JSON, formats it, and prints it
    print("{")
    i = 1
    for key, value in flattenedJSON.items():
        line = "     '{}{}{}{}".format(key, "':", value, "," if i < len(flattenedJSON) else "")
        print(line)
        i += 1
    print("}")


def unflattenOuter(flatDict, delim='/'):
    '''
    Takes a flat dictionary and unflattens it. Keys containing lists will not have a proper
    hierarchy after being processed by this function. For dictionaries that contain lists,
    this is meant to be followed up with a call to dictToList() below.

    Parameters:
    flatDict (dict): Flat dictionary to be unflattened.
    delim (str): Indicates how the keys are separated.

    Returns:
    dict: The unflattened dictionary. Dictionaries with lists will not be completely
        unflattened at this point.
    '''
    unflattenedDict = {}

    def unflattenOuter(unflatDict, keys, value):
        '''
        Takes an initially empty dictionary, a list of flattened keys & the corresponding value,
        and adds the keys and values to the dictionary in the necessary hierarchy.

        Parameters:
        unflatDict (dict): Initially empty dictionary. Keys and values are added to it in the
            correct hierarchy so long as the values are not parts of a list.
        keys (list): List of the flattened keys split up by their delimitter.
        value: The value that corresponds to the list of keys.
        '''
        for key in keys[:-1]:
            unflatDict = unflatDict.setdefault(key, {})
        # Add the last key-value pair to the dictionary assuming it was valid
        unflatDict[keys[-1]] = value

    # For each line in the flat dictionary, unflatten it
    for item in flatDict:
        unflattenOuter(unflattenedDict, item.split(delim), flatDict[item])
    
    return unflattenedDict


def unflatten(flatDict, delim='/'):
    '''
    Takes a flattened dictionary containing json data, and unflattens it.
    
    Parameters:
    flatDict (dict): The original flat dictionary
    delim (str): Delimitter used to separate keys
    
    Returns:
    dict: unflattened dictionary
    '''
    # Unflatten the dictionary, ignoring lists for now
    unflattenedDict = unflattenOuter(flatDict, delim)    

    def dictToList(object_, parentObject, parentObjectKey):
        '''
        Takes a dictionary and recursively handles the process of taking flattened lists and
        converting them back to regular json lists. Is meant to be called after unflattenOuter()
        has already processed the data due to the way it changes the hierarchy of lists.

        Parameters:
        object_ (dict): Dictionary that needs to be unflattened.
        parentObject (dict): Dictionary containing the parent objects to object_
        parentObjectKey (str): Key that corresponds to object_
        '''
        if isinstance(object_, dict):
            for key in object_:
                # There's another layer of objects to parse. Recursive case
                if isinstance(object_[key], dict):
                    dictToList(object_[key], object_, key)
            # The code in the try block will fail if the keys in 'object_' aren't integers
            try:
                # Keys represents the indices for the JSON list elements
                keys = [int(key) for key in object_]
                keys.sort()
            except (ValueError, TypeError):
                # Key is not the index of a list, so make keys an empty list.
                keys = []
            keysLength = len(keys)
            # Ensure that there is currently an list and
            # that the elements in 'keys' all correspond to the same list
            if (keysLength > 0 and sum(keys) ==
                int(((keysLength - 1) * keysLength) / 2) and keys[0] == 0 and
                    keys[-1] == keysLength - 1):
                # parentObject[parentObjectKey] currently contains list indices, so the value is reset
                parentObject[parentObjectKey] = []
                for keyIndex, key in enumerate(keys):
                    # Add the list elements to the dictionary
                    parentObject[parentObjectKey].append(object_[str(key)])
                    
    # Now enter the recursive function that handles the lists
    dictToList(unflattenedDict, None, None)
    return unflattenedDict

def main():
    PATH = "./test.json"
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        #replace all single quotes with double quotes
        rawJson = open(PATH, "r").read().replace("'", '"')
        #Load json into dictionary, 
        jsonDict = json.loads(rawJson)
        
        # Print original json
        print(jsonDict)
        
        # Get flattened json, format it and print it
        flattenedJSON = flatten(jsonDict)
        printFlattenedJSON(flattenedJSON)
        
        # Take flattened json, unflatten it, print it
        print(unflatten(flattenedJSON))
    else:
        print(PATH + " not found.")
    
main()
