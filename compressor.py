from collections import abc


class ObjectCompressor:
    """
    This is a class containing compress and decompress functions as described on https://github.com/Ontraport/Backend-Test
    """
    def compress(self, object_to_compress, path_so_far: str = "", dictionary: dict = None) -> dict:
        """
        This function compresses a multi-dimensional container of any size (tested with nested Python dictionaries and nested custom classes)
        and returns a compressed version of the original container as a Python dictionary
        """
        if(dictionary is None):
            dictionary = {}
        # If this is a Collection, it will always be Sized, but we want to handle Mappings slightly different, since they can contain nested objects
        if(isinstance(object_to_compress, abc.Collection)):
            # If this is a Mapping (e.g. a dictionary), iterate through keys and compress recursively
            if(isinstance(object_to_compress, abc.Mapping)):
                if(len(object_to_compress) > 0):
                    for attribute in object_to_compress.keys():
                        value = object_to_compress.get(attribute)
                        self.save_or_recurse(path_so_far + "/" + str(attribute), dictionary, value)
                else:
                    if(path_so_far):  # only add this object if it wasn't top level
                        self.save_or_recurse(path_so_far, dictionary, {}, True)
            # If this is a Sized Collection (e.g. a List), iterate through elements and compress recursively
            elif(isinstance(object_to_compress, abc.Sized)):
                if(len(object_to_compress) > 0):
                    for i in range(len(object_to_compress)):
                        value = object_to_compress[i]
                        self.save_or_recurse(path_so_far + "/" + str(i), dictionary, value)
                else:
                    if(path_so_far):  # only add this object if it wasn't top level
                        self.save_or_recurse(path_so_far, dictionary, [], True)
        # If this is a custom object, iterate through non-private attributes and compress
        else:
            filtered_attributes = list(filter(lambda x: not x.startswith('__'), dir(object_to_compress)))
            if(len(filtered_attributes) > 0):
                for attribute in filtered_attributes:
                    value = getattr(object_to_compress, str(attribute))
                    self.save_or_recurse(path_so_far + "/" + str(attribute), dictionary, value)
            else:
                if(path_so_far):  # only add this object if it wasn't top level
                    self.save_or_recurse(path_so_far, dictionary, {}, True)
        return dictionary

    def save_or_recurse(self, path_so_far: str, dictionary: dict, value, force_insert: bool = False) -> dict:
        """
        This helper function was introduced to minimize duplicate code in the compress(...) method
        """
        if(path_so_far.startswith("/")):
            path_so_far = path_so_far[1:]
        if (not isinstance(value, (float, int, str, bool, type(None))) and force_insert is False):
            return self.compress(value, path_so_far, dictionary)
        else:
            dictionary[path_so_far] = value
            return dictionary

    def decompress(self, compressedObject: dict) -> dict:
        """
        This function expands a compressed container into a dictionary representation of its original form
        NOTE: If a custom object was flattened, decompress will still return a dictionary representation
        """
        if(isinstance(compressedObject, abc.Collection)):
            if(isinstance(compressedObject, abc.Mapping)):
                resultObject = {}
                keys = compressedObject.keys()
                # For each key in the compressed object
                for attribute in compressedObject.keys():
                    pathList = attribute.split("/")
                    if(pathList[0].isnumeric() and isinstance(resultObject, abc.Mapping)):
                        resultObject = []
                    pointer = resultObject
                    # For each token in the path
                    for i in range(len(pathList)):
                        token = pathList[i]
                        if(isinstance(pointer, abc.MutableSequence)):  # We are in a list
                            if(token.isnumeric()):
                                if(int(token) < len(pointer)):  # Already exists in this list
                                    pointer = pointer[int(token)]
                                else:
                                    if(i < len(pathList) - 1 and pathList[i+1].isnumeric()):
                                        pointer.append([])
                                    elif(i == len(pathList) - 1):
                                        pointer.append(compressedObject[attribute])
                                    else:
                                        pointer.append({})
                                    pointer = pointer[-1]
                        else:  # We are in a Map
                            if(i < len(pathList) - 1):
                                if(pathList[i+1].isnumeric()):  # There is an intermediate array
                                    if(token not in pointer):
                                        pointer[token] = []
                                else:
                                    if(token not in pointer):
                                        pointer[token] = {}
                                pointer = pointer[token]
                            else:
                                pointer[token] = compressedObject[attribute]
                return resultObject
