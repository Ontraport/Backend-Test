#!/usr/bin/env ruby

def flatten( container )
  output = {}
  container.each do |key,val|
    if val.class == Hash
      flatten(val).each do |subkey,subval|
        output[key.to_s + "/" + subkey.to_s] = subval
      end
    elsif val.class == Array
      val.each_with_index do |subval, idx|
        output[key.to_s + "/" + idx.to_s] = subval
      end
    else
      output[key] = val
    end
  end
  output
end

def deflatten( container )
  output = {}
  container.each do |key,val|
    keys = key.split("/")
    ref = output
    keys.each_with_index do |subkey, index|
      # apologies for the regex. again: assumption here is that an int path always refers to an array index
      if index < keys.length - 1
        if !!(keys[index+1] =~ /^[0-9]*$/) && !ref[subkey]
          ref[subkey] = []
        elsif !ref[subkey]
          ref[subkey] = {}
        end
        ref = ref[subkey]
      else
        if ref.class == Array
          ref.push( val )
        else
          ref[subkey] = val
        end
      end
    end
  end
  output
end

unflattened = {
    'one' =>
    {
        'two' => 3,
        'four' => [5,6,7]
    },
    'eight' =>
    {
        'nine' =>
        {
            'ten' => 11
        }
    }
}

flattened = {
    'one/two' => 3,
    'one/four/0' => 5,
    'one/four/1' => 6,
    'one/four/2' => 7,
    'eight/nine/ten' => 11
}

print "#flatten "
if flatten( unflattened ) == flattened
  puts "works! :)"
else
  puts "FAILED! :("
end

print "#deflatten "
if deflatten( flattened ) == unflattened
  puts "works! :)"
else
  puts "FAILED! :("
end
