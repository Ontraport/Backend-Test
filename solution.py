"""
DFS approach: go through each element until its leaf node is found, then add it to a dict 
"""
def solution1(input) -> dict:
	def flatten_mdim(elem, curr_path="", flattened_output={}):
		if type(elem) != dict and type(elem) != list:   #not iterable, reached leaf node
			flattened_output[curr_path[:-1]] = elem

		if type(elem) == dict:
			for key in elem:
				flatten_mdim(elem[key], curr_path + f"{key}/", flattened_output)

		if type(elem) == list or type(elem) == tuple:  
		#supports both mutable and immutable python arrays 
			for i in range(len(elem)):
				flatten_mdim(elem[i], curr_path + f"{i}/", flattened_output)

		return flattened_output

	return flatten_mdim(input)

def solution2(input) -> dict:
	def update_dict(unflattened, seen_path, components, subpath, value, i):
		local_dict = unflattened
		for key in seen_path:
			local_dict = local_dict[key]
				
		try:
			subpath_index = int(subpath)
			if (subpath_index == 0):   #underlying element is a list or tuple but not a dict 
				if i == (len(components) - 1):
					local_dict[subpath_index] = value
				else: 
					local_dict[subpath_index] = [ ]
			if (subpath_index > 0):
				local_dict[subpath_index] = value
				
		except:  #if element is not an index, it is a key so underlying element is a dict 
			if i == (len(components) - 1):
				local_dict[subpath] =  value
			else:
				local_dict[subpath] = {}
							
	def get_dict(unflattened, seen_path):
		curr_dict = unflattened
		for key in seen_path:
			curr_dict = curr_dict[key]
		return curr_dict
	
	def reverse(paths, unflattened={}):
		for path in paths:
			components = path.split("/")
			for i in range(len(components)):
				subpath = components[i] 
				seen_path = [components[j] for j in range(i)]
				if subpath not in get_dict(unflattened, seen_path):
					update_dict(unflattened, seen_path, components, subpath, paths[path], i)
		return unflattened
		
	return reverse(input)
	
test = { "one/two":3, "one/four/0":5, "one/four/1":6, "one/four/2": 7, "eight/nine/ten":11 }
print(solution2(test))