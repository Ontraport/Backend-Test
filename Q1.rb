def compile_helper(multiD, path, oneD)
    if not path.eql?("")
        path = path + "/"
    end

    multiD.each do |key, value|

        if value.kind_of?(Hash)
            oneD = compile_helper(value, path + key.to_s, oneD)
        elsif value.kind_of?(Array) then
            i = 0
            value.each do |element|
                oneD.store(path + key.to_s + "/" + i.to_s, element)
                i += 1
            end
        else 
            oneD.store(path + key.to_s, value)
        end

    end

    return oneD
end

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