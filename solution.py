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
	
