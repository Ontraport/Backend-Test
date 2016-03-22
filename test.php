<?php
/**
 * 1) Write a function that accepts a multi-dimensional container of any size
 * and converts it into a one dimensional associative array whose keys are
 * strings representing their value's path in the original container.
 *
 * @param array $multi the input array.
 * @return array single-dimensional representation.
 */
function manyToOne($multi, $prefix = array())
{
    $flattened = array();
    foreach ($multi as $key => $value) {
        $currentPrefix = $prefix;
        $currentPrefix[] = $key;
        if (is_array($value)) {
            $children = manyToOne($value, $currentPrefix);
            $flattened = array_merge($flattened, $children);
        } else {
            $useKey = implode('/', $currentPrefix);
            $flattened[$useKey] = $value;
        }
    }
    return $flattened;
}

/**
 * 2) Now write a separate function to do the reverse.
 *
 * @param $single the input array.
 * @return array the multi-dimensional representation.
 */
function oneToMany($single)
{
    $multi = array();
    foreach ($single as $key => $value) {
        $parts = explode('/', $key);
        $reference = &$multi;
        foreach ($parts as $part) {
            if (!isset($reference[$part])) {
                $reference[$part] = array();
            }
            $reference = &$reference[$part];
        }
        $reference = $value;
    }
    return $multi;
}

/**
 * Just a helper function to keep the code below tidy.  Prints the JSON
 * encoded version of $variable, along with a comment.
 *
 * @param string $comment
 * @param mixed $variable
 */
function printIt($comment, $variable)
{
    echo($comment . "\n"
        . json_encode($variable, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)
        . "\n\n");
}

/////////////////////////////////////
// Main routine.  Tests the functions above.

try {
    // Prep the input
    $multi = json_decode(
        '{
            "one":
            {
                "two": 3,
                "four": [ 5,6,7]
            },
            "eight":
            {
                "nine":
                {
                    "ten":11
                }
            }
        }',
        true
    );
    printIt('starting from:', $multi);

    // Test manyToOne()
    $single = manyToOne($multi);
    printIt('flattened to:', $single);

    // Test oneToMany()
    $many = oneToMany($single);
    printIt('expanded to:', $many);
} catch (Exception $e) {
    echo('Caught exception: '.$e->getMessage()."\n");
    exit(1);
}
echo("Done\n");
exit(0);
