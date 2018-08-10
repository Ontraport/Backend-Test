#!/usr/bin/env ruby

##
# Question 1: Write a function that accepts a multi-dimensional container of any 
# size and converts it into a one dimensional associative array whose keys are strings 
# representing their value's path in the original container.

# This helper function takes the multi-dimensional container and iterates through each 
# element and builds the final one-dimensional associative array in a recursive down-top order.
#   1. For each element in the container check the values to see 
#        if it's another container, array or a number.
#   2. If map, recusively call the helper function on that map object with updated path 
#          and current associative array (oneD).
#   3. Else, store key and the value to current associative array (oneD).
#
#     
# params
# => "multiD" is the multi dimensional container that is passed.
# => "path" is the parameter to remember and create the current path.
# => "oneD" is the one-dimensional array that is updated and populated (since Ruby is pass by value)
#           it needs to be updated and reassigned.



def compile_helper(multiD, path, oneD)
    # Check if the helper function has called for the first time.
    if not path.eql?("")
        path = path + "/"
    end

    multiD.each do |key, value|

        # If the value is a nother container, recursively call the helper function and pass the value, 
        # the current path as well as the current key and finally the associative array.
        if value.kind_of?(Hash)
            oneD = compile_helper(value, path + key.to_s, oneD)

        # If the value is an array, create a new path for each element. Use index as the path.
        elsif value.kind_of?(Array) then
            i = 0
            value.each do |element|
                oneD.store(path + key.to_s + "/" + i.to_s, element)
                i += 1
            end
        # Else, store the path as the key and the number as the value.
        else 
            oneD.store(path + key.to_s, value)
        end

    end

    return oneD
end

#Main function, calls the helper function also creates a initial empty map.
#Param
# => "nstedMap" is the multi-dimensional container of any size.\

def compile_multi(nstedMap)
    oneDArray = Hash.new
    puts compile_helper(nstedMap, "", oneDArray)
end

example = {
  "one" => { 
    "two" => 3,
    "four" => [5,6,7]
  },
  "eight" => {
    "nine" => {
        "ten" => 11
    }
  }
}

compile_multi(example)