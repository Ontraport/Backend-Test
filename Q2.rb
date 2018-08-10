def decomp_helper(partMap)
	temp = partMap.keys[0].split("/", 2)[0]
	tempMap = Hash.new
	finalMap = Hash.new
	temparray = [];
	partMap.each do |key, value|

		toks = key.split("/", 2)

		if toks[0] == temp

			isArray = Integer(toks[1]) rescue false

			if toks[1].instance_of?(NilClass)
				finalMap.store(toks[0], value)
			elsif isArray
				temparray << value
				puts temparray
			else
				tempMap.store(toks[1], value)
			end

		else 

			if not temparray.empty?
				finalMap.store(temp, temparray)
				temparray.clear
			elsif not tempMap.empty?
				finalValue = decomp_helper(tempMap)
				finalMap.store(temp, finalValue)
				tempMap.clear
			end
			
			temp = toks[0]
			redo
		end
	end


	if not temparray.empty?
			finalMap.store(temp, temparray)
			temparray = Array.new
	elsif not tempMap.empty?
		finalValue = decomp_helper(tempMap)
		finalMap.store(temp, finalValue)
	end

	return finalMap
end



def decomp_single(oneD)
	manyD = Hash.new
	temp = oneD.keys[0].split("/", 2)[0]
	tempMap = Hash.new
	oneD.each do |key, value|
		toks = key.split("/", 2)
		if toks[0] == temp
			tempMap.store(toks[1], value)
		else 
			finalValue = decomp_helper(tempMap)
			manyD.store(temp, finalValue)
			temp = toks[0]
			tempMap = Hash.new
			redo
		end
	end
	finalValue = decomp_helper(tempMap)
	manyD.store(temp, finalValue)
	puts manyD
end

example = {
	"one/two" => 3,
	"one/four/0" => 5,
	"one/four/1" => 6,
	"one/four/2" => 7,
	"eight/nine/ten" => 11
    }


decomp_single(example)
