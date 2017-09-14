<?php

use BackendTest\ArrayManipulator as ArrayManipulator;

include_once "ArrayManipulator.php";

$multi_dimensional_array = array(
    'one' => array(
      'two' => 3,
      'four' => array(
        5,6,7
      )
    ),
    'eight' => array(
      'nine' => array(
        'ten' => 11
      )
    )
);

$objArrayManuplator = new ArrayManipulator();

$associative_array = $objArrayManuplator->doConvertToAssociativeArray(
  $multi_dimensional_array
);

$revered_array = $objArrayManuplator->doReverseToOriginalArray($associative_array);

print "<pre>" . print_r($associative_array,1) . "</pre>";
print PHP_EOL;
print "<pre>" . print_r($revered_array,1) . "</pre>";
