def decomp_alt(partMap)
	finalMap = Hash.new
	partMap.each do |key, value|
		parent, child = key.split("/", 2)
		isArray = Integer(child) rescue false

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
		if value.instance_of?(Hash)
			finalMap[key] = decomp_alt(value)
		end
	end
	return finalMap
end

def decomp_single(oneD)
	puts decomp_alt(oneD)
end

example = {
	"one/two" => 3,
	"one/four/0" => 5,
	"one/four/1" => 6,
	"one/four/2" => 7,
	"eight/nine/ten" => 11
    }


decomp_single(example)
