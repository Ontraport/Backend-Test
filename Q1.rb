def comp_helper(manyD, path, oneD)
    manyD.each do |key, value|
        if value.kind_of?(Hash)
            oneD = comp_helper(value, path + "/" + key.to_s, oneD)
        elsif value.kind_of?(Array) then
            i = 0
            value.each do |element|
                oneD.store(path + "/" + key.to_s + "/" + i.to_s, element)
                i += 1
            end
        else 
            oneD.store(path + "/" + key.to_s, value)
        end
    end
    return oneD
end

def comp_multi(nstdMap)
    oneD = Hash.new
    nstdMap.each do |key, value|
        if value.kind_of?(Hash)
            ondD = comp_helper(value, key.to_s, oneD)
        else 
            oneD.store(key.to_s + "/", value)
        end
    end
    puts oneD
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

comp_multi(example)

#start time = 11:44am
#finish time = 1:02pm