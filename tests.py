import solution

def run_tests(testcases, expected_results):
	for n in range(len(testcases)):
		print(f"Running tests for problem{n+1}...")
		tests, expected = testcases[n], expected_results[n]
		for i in range(len(tests)):
			if n +1 == 1:  #test problem 1
				actual = solution.solution1(tests[i])
			if n + 1 == 2:  # test problem 2
				actual = solution.solution2(tests[i])

			if actual == expected[i]:
				print(f"Test{i+1} passed")
			else:
				print(f"Test{i+1} failed")


"""
Test cases for Problem 1 (Flattening a multidimensional container into an associative array):
	- solution1() is the top-level for flatten_mdim() function in solution.py which solves this  
"""

"""
test1 was provided in the github 
"""

test1 = {
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

"""
test2 is a further nested case of test1
"""

test2 = {
    'one':
    {
        'two': {'nested1_deep':{'nested2_deep1':3, 'nested2_deep2':9}},
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

"""
test3 has a nested dict containing an array
"""

test3 = {
    'one':
    {
        'two': 3,
        'four': [ {'key':[3,4,7]},6,7],
    },
    'eight':
    {
        'nine':
        {
            'ten':11
        }
    }
}	

"""
empty dict input -> should return empty output
"""
test4 = {}

"""
first key encountered is not nested
"""
test5 = {"key1":5,"key2":[{"key3":[8,9]},2,3]}  

"""
input is not a dict
"""
test6 = [1,2,3]

expected1 = { "one/two":3, "one/four/0":5, "one/four/1":6, "one/four/2": 7, "eight/nine/ten":11 }
expected2 = { "one/two/nested1_deep/nested2_deep1":3, "one/two/nested1_deep/nested2_deep2":9, "one/four/0":5, "one/four/1":6, "one/four/2": 7, "eight/nine/ten":11 }
expected3 = { "one/two": 3, "one/four/0/key/0":3, "one/four/0/key/1": 4, "one/four/0/key/2": 7, "one/four/1": 6, "one/four/2": 7, "eight/nine/ten":11 }
expected4 = {}
expected5 = {"key1": 5, "key2/0/key3/0":8, "key2/0/key3/1":9, "key2/1":2, "key2/2": 3}
expected6 = { '0':1, '1':2, '2':3}

"""
Test cases for Problem 2 (Reversing the associative array back into the original)
	- solution2() is the top-level for 
"""

tests = [[test1, test2, test3, test4, test5, test6], []]


expected = [[expected1, expected2, expected3, expected4, expected5, expected6], []]

run_tests(tests, expected)

