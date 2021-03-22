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
			int_subpath = int(subpath)
			return int_subpath
		except:
			return subpath
	
	def build_container(container, seen_path, subpaths, i, value):
		local_container = container
		for key in seen_path:
	#		local_container = local_container[key]
			try:
				local_container = local_container[int(key)]
			except ValueError:
				local_container = local_container[key]		
		try:
			subpath = int(subpaths[i])
			try:
				present = (local_container[subpath] in local_container)
			except:
				present = False
		except ValueError:
			subpath = subpaths[i]
			present = (subpath in local_container)
			
	#	if subpath not in local_container:
		if not present:
			try:
				subpath_index = int(subpath)
				if i == (len(subpaths) - 1):
					local_container.append(value)	
				else:	
					try:
						next_path = int(subpaths[i+1])
						if local_container == []:
							local_container.append([])
						else:
							local_container[subpath] = []
					except ValueError:
						local_container.append({})
				
			except ValueError:  #if element is not an index, it is a key so underlying element is a dict 
				if i == (len(subpaths) - 1):
					local_container[subpath] =  value
				else:
					try:
						next_path = int(subpaths[i+1])
						if local_container == []:
							local_container.append([])
#							local_container[subpath] = []
						else:
							local_container[subpath] = []
					except ValueError:
						local_container[subpath] = {}
	
	def reverse(paths, container={}):
		try:
			first_elem = paths[0]
			container = []
		except:
			container = {}
		
		for path in paths:
		#	subpaths = [make_int_if_array(subpath) for subpath in path.split("/")] 
			subpaths = [subpath for subpath in path.split("/")]
			for i in range(len(subpaths)):
				build_container(container, [subpaths[j] for j in range(i)], subpaths, i, paths[path])
		return container
		
	return reverse(input)