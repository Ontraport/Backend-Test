import pdb

container = {    'one':
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

def flatten(container):
	
	flat = {}

	for key in container:
		
		valueType = type(container[key])
		
		if valueType is dict:
			flatChild = flatten(container[key])
			for childKey in flatChild:
				flat[key + '/' + childKey] = flatChild[childKey]
		elif valueType is list:
			for index, value in enumerate(container[key]):
				flat[key + '/' + str(index)] = value
		elif valueType is str or int:
			flat[key] = container[key]

	return flat

def mergeList(list1, list2):
	for index, value in enumerate(list2):
		if value is not 0:
			list1[index] = list2[index]

	return list1


def deflatten(flatContainer):

	container = {}

	for key in flatContainer:
		if "/" in key:
			parentKey, childKey = key.split("/", 1)

			if childKey.isdigit() is True:
				if parentKey not in container:
					container[parentKey] = []
				if len(container[parentKey]) < int(childKey) + 1:
					for i in range(len(container[parentKey]), int(childKey)):
						container[parentKey].append(0)

				container[parentKey].append(flatContainer[key])
				continue

			child = {}
			child[childKey] = flatContainer[key]

			children = deflatten(child)

			if parentKey not in container:
				container[parentKey] = {}

			for key in children:
				if key in container[parentKey]:
					if len(container[parentKey][key]) < len(children[key]):
						container[parentKey][key] = mergeList(children[key], container[parentKey][key])
					else:
						container[parentKey][key] = mergeList(container[parentKey][key], children[key])
					
				else:
					container[parentKey][key] = children[key] 
		else:
			container[key] = flatContainer[key]
	return container

flat = flatten(container)
print(flat)
print(deflatten(flat))