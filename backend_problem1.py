''' 
Author: Jazarie Thach
Description: Write a function that accepts a multi-dimensional container of any size and converts it into a one dimensional associative array whose keys are strings representing their value's path in the original container.
'''

def _multiToOne(container, key_str, output):
	for key, val in container.iteritems():
		current_key = key_str + key + "/"

		if (isinstance(val, list)):
			# print "list key:{} val:{}".format(current_key, val)
			index = 0
			for elem in val:
				list_key = "{}{}".format(current_key,index)
				output[list_key] = elem
				index = index + 1
		elif (isinstance(val, dict)):
			_multiToOne(val, current_key, output)
			# print "dict key:{} val:{}".format(current_key, val)
		else:
			current_key = key_str + key
			# print "else {}:{}".format(current_key, val)
			output[current_key] = val


		
		# print "key {}".format(key)
		# print "val {}".format(val)

def multiToOne(container):
	output = {}
	_multiToOne(container, "", output)
	return output


test_input = {
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

# container = {'one': {'two': 3, 'four': [ 5,6,7]}, 'eight': {'nine': {'ten': 11}}}
	
print multiToOne(test_input)


