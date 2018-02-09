<?php

spl_autoload_register(function($class){
    include $class.".php";
});

if (count($argv) < 3) {
    die("\n\n\n
        Arguments required:\n
        1. command: multi or one\n
        2. the path to the json file
\n\n\n");
}

$command   = $argv[1];
$file_name = $argv[2];
$separator = null;

if (isset($argv[3])) {
    $separator = $argv[3];
}

$input = json_decode(file_get_contents($file_name), true);

if(!is_array($input)) {
    die("\n\n\nCorrupted JSON file\n\n\n");
}

// show input
echo "Input array:\n";
print_r($input);
echo "\n";

$converter = ConverterFactory::getConverter($command, $input, $separator);
$result = $converter->convert();

print_r($result);
