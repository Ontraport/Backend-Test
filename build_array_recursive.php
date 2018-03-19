<?php
/*
This is the first part of the test.
Execute script from cmd line.
T.Y.
*/

function buildArray($object_array, &$final_array = [], $prefix = []) {
    foreach ($object_array as $key => $value) {
        $prefix[] = $key ;

        if (is_array($value) || is_object($value)) {
            buildArray($value, $final_array, $prefix);
        } else {
            $final_array[implode('/', $prefix)] = $value ;
        }

        $val = array_pop($prefix);
    }
}

$json_str = "{
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
}";

//string provided is not valid JSON so let's make it valid JSON
$json_str = str_replace("'", '"', $json_str);

$object = json_decode($json_str);

buildArray($object, $final_array);

print_r($final_array);
