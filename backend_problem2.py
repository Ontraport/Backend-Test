''' 
Author: Jazarie Thach
Description: Write a function that accepts a one dimensional associative array into a multi-dimensional container according to the path of the key.
'''

''' Sets value at given index in value_list. If index not set, fills undeclared indices until given index with None and then sets value. '''
def add_item(value_list, index, val):
	try:
		value_list[index] = val
	except IndexError:
		for x in range(index-len(value_list)+1):
			value_list.append(None)
		value_list[index] = val

''' Returns True if string s is an integer, otherwise False is returned '''
def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

''' Raises an error if the key was assigned to before. 'toList' and 'toDict' are booleans that tell if we are adding our element to that respective container '''
def error_if_set(path, toList, toDict):
	if isinstance(path, dict):
		if not toDict:	# check if adding to dict
			if path: 	# dictionary not empty
				raise KeyError ("Current key has already been set to {}".format(path))
	elif isinstance(path, list):
		if not toList: # check if adding to list
			raise KeyError ("Current key has already been set to {}".format(path))
	else:
		raise TypeError ("Container type not supported")


def _oneToMulti(container, output):
	for key, val in container.iteritems():
		tmp = output
		key_list = key.split('/')
		for elem in key_list:
			if is_int(elem):
				error_if_set(prev[prev_idx], True, False)
				if not isinstance(prev[prev_idx], list):
					prev[prev_idx] = []
				add_item(prev[prev_idx], int(elem), val)
				prev_idx = elem	
			else:
				prev = tmp
				prev_idx = elem	
			 	if elem not in tmp:
					error_if_set(tmp, False, True)
				 	tmp[elem] = {}
				tmp = tmp[elem]

		if not is_int(prev_idx):
			error_if_set(prev[prev_idx], False, False)
			prev[prev_idx] = val

def onetoMulti(container):
	output = {}
	_oneToMulti(container, output)
	return output


test_input = {
	'one/two':3,
	'one/four/0':5,
	'one/four/1':6,
	'one/four/2':7,
	'eight/nine/ten':11
}

error_input1 = {
	'one/four/0':5,
	'one/four/1':6,
	'one/four/2':7,
	'one/four':10 # error: cannot set value since one/four already set to list
}

error_input2 = {
	'one/four/0':5,
	'one/four/1':6,
	'one/four/2':7,
	'one/four/five':10 # error: cannot expand container since one/four already set to list
}

print onetoMulti(test_input)
