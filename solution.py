"""
DFS approach: go through each element until its leaf node is found, then add it to a dict 
"""
def solution1(input) -> dict:
	def flatten_container(elem, curr_path="", flattened_output={}):
		if type(elem) != dict and type(elem) != list:   #not iterable, reached leaf node
			flattened_output[curr_path[:-1]] = elem

		if type(elem) == dict:
			for key in elem:
				flatten_container(elem[key], curr_path + f"{key}/", flattened_output)

		if type(elem) == list:  
			for i in range(len(elem)):
				flatten_container(elem[i], curr_path + f"{i}/", flattened_output)

		return flattened_output

	return flatten_container(input)

def solution2(input) -> dict:
	""" Takes a subpath and converts it into an int type if possible, otherwise returns as is (str) """
	def make_int_if_array(subpath): 
		try:
			return int(subpath)
		except:
			return subpath
			
	""" 4 cases and different operations required based on current underlying object and next underlying object  """		
	def initialize_next_object(next_subpath, curr_subpath, local_container):
		if type(curr_subpath) == int and type(next_subpath) == int:  #nested array 
			local_container.append([])
		if type(curr_subpath) == int and type(next_subpath) == str:  #dict inside array 
			local_container.append({})
		if type(curr_subpath) == str and type(next_subpath) == int: #array inside dict 
			local_container[curr_subpath] = []
		if type(curr_subpath) == str and type(next_subpath) == str: #nested dict 
			local_container[curr_subpath] = {}
	
	def build_container(container, seen_path, subpaths, i, value):
		local_container = container
		for key in seen_path: 
			local_container = local_container[key]  #run through all prior keys to index container down to most recent state
		
		subpath = subpaths[i]
		if type(subpath) == int:
			in_container = (subpath < len(local_container))		#check if index in array  	
		else:
			in_container = (subpath in local_container)   #check if key in dict 

		if not in_container:  #only build subpath in the container if it doesn't exist already
			if i == len(subpaths) - 1 and type(subpath) == int:  
				local_container.append(value)
			elif i == len(subpaths) - 1 and type(subpath) == str:  
				local_container[subpath] = value   
			else:
				initialize_next_object(subpaths[i+1], subpath, local_container)
						 
	def reverse(paths, container={}):
		try:
			array = list(paths.keys())[0]   
			first_val = int(array.split("/")[0])  #checking first val, if it is array index then input is array 
			container = []  #set container to array when input is mdim array
		except:
			container = {}

		for path in paths:
			subpaths = [make_int_if_array(subpath) for subpath in path.split("/")]  #preprocess: cast array indices to int 
			for i in range(len(subpaths)):
				build_container(container, [subpaths[j] for j in range(i)], subpaths, i, paths[path])			
		return container
			
	return reverse(input)