<?php

class ConvertContainer
{
    /**
     * Pass multi-dimensional container to get dimensional associative array
     * @param array $array
     * @param string $parentKey
     * @param array $result
     * @return array
     */
    public function convert($array, $parentKey = '', $result = []) {

        $parentKey = $parentKey . ($parentKey == '' ? '' : '/');
        if(empty($array)){
            return [];
        }

        foreach ($array as $key => $value) {
            // if value is also array check it recursively to build final array
            if(is_array($value)) {
                $result = $this->convert($value,  $parentKey . $key, $result);
            } else {
                //we reached end or array path lets add $parentKey, $key and value to the result
                $result[$parentKey . $key] = $value;
            }
        }
        return $result;
    }

    /**
     * Convert associative array into multi-dimensional container
     * @param array $array
     * @return array
     */
    public function reverseConvert($array) {
        $result = [];
        if(empty($array)){
            return [];
        }

        foreach ($array as $key => $value) {
            $keysArr = (explode('/', $key));
            //build multi dimensional array from each element of array
            $tmpArr = $this->buildMultiDimensionalArray($keysArr, $value);
            $result = array_replace_recursive($result, $tmpArr);
        }

        return $result;
    }

    /**
     * @param array $keys
     * @param string $value
     * @return array
     */
    public function buildMultiDimensionalArray($keys, $value) {

        $result = $value;
        $keys = array_reverse($keys);

        foreach ($keys as $key) {
            $temp = $result;
            $result = [];
            $result[$key] = $temp;
        }

        return $result;
    }
}