<?php
function array_flatten($array) { 
  	if (!is_array($array)) { 
    	return FALSE; 
  	}
  	$result = array(); 
  	foreach ($array as $key => $value) { 
    	if (is_array($value)) {
			$value=array_combine(
				array_map(create_function('$k', 'return "'.$key.'/".$k;'), array_keys($value))
				, $value
			);
      		$result = array_merge($result, array_flatten($value)); 
    	} 
    	else { 
      		$result[$key] = $value; 
    	} 
  	} 
  	return $result; 
}
function array_expand($array) { 
  	if (!is_array($array)) { 
    	return FALSE; 
  	}
	$result = array(); 
  	foreach ($array as $key => $value) { 
    	set_array_value($result, explode("/", $key), $value);
  	} 
  	return $result; 
}
function set_array_value(&$array, $indexes, &$value){
	if (count($indexes) == 1){
    	return $array[reset($indexes)] = $value;
  	}
  	$index = array_shift($indexes);
  	return set_array_value($array[$index], $indexes, $value);
}

$array=array(
	'one'=>array(
        'two' => 3,
        'four' => array( 5,6,7)
    ),
    'eight'=>array(
        'nine' =>array(
			'ten'=>11,
			"eleven"=>array(
				'one'=>array(
					'two' => 3,
					'four' => array( 5,6,7)
				),
			)
		)
    )
);

echo "Original array: <br />";
print_r($array);

$flattened=array_flatten($array);
echo "<br />Flattened array: <br />";
print_r($flattened);

$expanded=array_expand($flattened);
echo "<br />Expanded array: <br />";
print_r($expanded);