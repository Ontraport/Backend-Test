<?php

/**
 * Ontraport Backend Skills Test Submission
 * PHP Version 7
 *
 * @category  None
 * @package   None
 * @author    Brad Dobson <brad@bdobson.net>
 * @copyright 2019 Ontraport - All Rights Reserved
 * @license   http://www.ontraport.com/ Proprietary
 * @link      None
 */

/**
 * SkillsAssessment class
 *
 * @category None
 * @package  None
 * @author   Brad Dobson <brad@bdobson.net>
 * @license  http://www.ontraport.com/ Proprietary
 * @link     None
 */
class SkillsAssessment
{

    /*
     * Notes
     * - I departed slightly from the test description:
     * - the examples used single quotes. Since it wasn't explicitly stated
     *   I assumed I could user double quotes so that the data could be easily
     *   parsed by json functions. It would be trivial to add something to
     *   convert the quotes first.
     * - Since the json function allows it to pull the whole thing in as an
     *   associative array, I've interpreted 'container' to mean 'array', which
     *   allows the traversal to be a little easier.
     * - I wouldn't have necessarily wrapped this in a class, but phpunit only
     *   really seems to like testing classes.
     */

    /**
     * Function flattenArray
     *
     * @param array $inputArr Input array
     *            
     * @return array Walk a multidimensional array (basically a tree). Keep 
     *               running track of the current stack of levels and their 
     *               names. For each leaf, output the merged stack path as a 
     *               single key with the associated value.
     */
    function flattenArray($inputArr)
    {
        $elemStack = array();
        $pathStr = "";
        $outputArr = array();
        $currentElem = $inputArr;
        $key = key($currentElem);
        while ($currentElem != null) {
            if (array_key_exists($key, $currentElem) 
                && is_array($currentElem[$key])
            ) {
                /*
                 * subarray: push onto the stack, build the path string deeper,
                 * walk to next deeper level.
                 */
                array_push($elemStack, $currentElem);
                $pathStr .= $key . "/";
                $currentElem = $currentElem[$key];
            } else {
                if (array_key_exists($key, $currentElem) 
                    && $currentElem[$key] != ""
                ) {
                    /* leaf: make the assignment in the flattened array */
                    $outputArr[$pathStr . $key] = $currentElem[$key];
                }
                if (next($currentElem) === false) {
                    /*
                     * done with subarray: pop from stack, shorten path string
                     * walk to next at this level.
                     */
                    $currentElem = array_pop($elemStack);
                    $lastslash = strrpos($pathStr, "/", strlen($pathStr) - 1);
                    $pathStr = substr($pathStr, 0, $lastslash);
                    if ($currentElem != null) {
                        next($currentElem);
                    }
                }
            }
            if ($currentElem != null) {
                $key = key($currentElem);
            }
        }
        return ($outputArr);
    }

    /**
     * Function deepenArray
     *
     * @param array $inputArr Input array
     *            
     * @return array Take a single-dimensional array where each key itself 
     *               represents further subarrays. Explode each key and create 
     *               a multidimensional array structure. This reverses 
     *               flattenArray(). Also considered 'embiggenArray()' as a more
     *               cromulent function name.
     */
    function deepenArray($inputArr)
    {
        $outputArr = array();
        foreach ($inputArr as $arrayLevels => $value) {
            $current = &$outputArr;

            /* Create an array of levels from the original key value */
            $keys = explode("/", $arrayLevels);
            foreach ($keys as $key) {
                /* build the subarray levels as we go */
                if (! isset($current[$key])) {
                    $current[$key] = array();
                }
                $current = &$current[$key];
            }
            /* do the assignment */
            $current = $value;
        }
        return ($outputArr);
    }
}


?>