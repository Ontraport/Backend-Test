#!/usr/bin/env ruby

##
# Question 2: Convert a one dimensional associative array created from question 1
# back to a multi-dimensional container of any size.


# This helper function takes the elements of the array and creates containers according to the path
# in a recursive top-down order. 
# 	1. It parses the parent and the rest(child) of the path
# 	2. Checks for various conditions such as is rest of the path nil? and is the path part of a array?
# 	3. Push the appropriate values to the variable finalMap (maps, values, arrays).
# 	4. Finally, iterate through finalMap to see if the value is a instance of a map, 
#	   recursively call on that map object.
#
# 	
# param
# => "partMap" is initally the complete one dimensional associative array, 
#    then partial maps where a paths still exist.

def decompile_helper(partMap)
	finalMap = Hash.new

	partMap.each do |key, value|
		parent, child = key.split("/", 2)

		#Check if the child is part of a array.
		isArray = Integer(child) rescue false

		#Cases to check for before populating finalMap.
		if child.instance_of?(NilClass)
			finalMap[parent] = value
		elsif isArray && finalMap.key?(parent)
			finalMap[parent] << value
		elsif finalMap.key?(parent)
			finalMap[parent][child] = value
		elsif isArray
			finalMap[parent] = [value]
		else
			finalMap[parent] = { child => value }
		end
	end

	finalMap.each do |key, value|
		#Recursively call if the path still exists (i.e. value is a map).
		if value.instance_of?(Hash)
			finalMap[key] = decompile_helper(value)
		end
	end

	return finalMap
end

# Main function, calls the helper function.
# param
# => "oneDArray" is the one dimensional associative array to be converted.

def decompile_single(oneDArray)
	puts decompile_helper(oneDArray)
end

example = {
	"one/two" => 3,
	"one/four/0" => 5,
	"one/four/1" => 6,
	"one/four/2" => 7,
	"eight/nine/ten" => 11
    }


decompile_single(example)
