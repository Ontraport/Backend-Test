<?php
/*
This is the second part of the test.
Execute script from cmd line.
T.Y.
*/

function toJsonStr($array, &$result=array()) {
    foreach($array as $key => $value) {
        $path = explode('/', $key);
        $temp =& $result;    
        foreach($path as $key) {
            $temp =& $temp[$key];
        }
        $temp = $value;
    }
    $result = json_encode($result);
}

$array = [
	'one/two' => 3,
	'one/four/0' => 5,
	'one/four/1' => 6,
	'one/four/2' => 7,
	'eight/nine/ten' => 11,
];

toJsonStr($array, $result);

print_r($result);
echo "\n";
