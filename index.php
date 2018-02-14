<?php

require 'ConvertContainer.php';

$object = new ConvertContainer();
$array = [
    'two' => [
        1,
        ['xx' => 10, 'yy' => 20, 'zz' => 30],
        3,
        'one' => 1
    ]
];

$result = $object->convert($array);

echo '<h1>Convert to associative array</h1>';
echo '<pre>';
print_r($result);
echo '</pre>';

$result = $object->reverseConvert($result);
echo '<h1>Convert back to multi dimensional array</h1>';
echo '<pre>';
print_r($result);
echo '</pre>';