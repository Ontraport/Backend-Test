
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
		
		#get value type
		valueType = type(container[key])
		
		if valueType is dict:
			#recursively flatten the child
			flatChild = flatten(container[key])
			for childKey in flatChild:
				flat[key + '/' + childKey] = flatChild[childKey]
		elif valueType is list:
			for index, value in enumerate(container[key]):
				#append index to key
				flat[key + '/' + str(index)] = value
		elif valueType is str or int:
			flat[key] = container[key]

	return flat

def deflatten(flatContainer):

	container = {}

	for key in flatContainer:
		if "/" in key:
			parentKey, childKey = key.split("/", 1)

			#recursively deflatten the child
			child = {}
			child[childKey] = flatContainer[key]
			children = deflatten(child)

			if parentKey not in container:
				container[parentKey] = {}

			for key in children:

				#if key is present already, it is a list
				if key in container[parentKey]:

					#if list not created, create (dict->list)
					if type(container[parentKey][key]) is not list:
						valList = []

						#the key becomes the index of element in list
						gkey = list(container[parentKey][key].keys())[0]
						
						#append zeroes to get desired length
						for i in range(int(gkey) + 1):
							valList.append(0)

						#update list entry
						valList[int(gkey)] = container[parentKey][key][gkey]

						#update list to container
						container[parentKey][key] = valList


					#insert new element into list
					valList = container[parentKey][key]
					gkey = list(children[key].keys())[0]

					#append zeroes to get desired length
					if len(valList) < int(gkey) + 1:
						for i in range(len(valList), int(gkey)+1):
							valList.append(0)
					
					#update list entry
					valList[int(gkey)] = children[key][gkey]
						
				else:
					container[parentKey][key] = children[key] 
		else:
			container[key] = flatContainer[key]
	
	return container


def main():
	print('Original Container', container)
	flat = flatten(container)
	print('Flattened Conatainer', flat)
	deflat = deflatten(flat)
	print('Deflattened Container', deflat)

main()