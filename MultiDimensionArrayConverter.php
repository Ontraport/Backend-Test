<?php

class MultyDimensionArrayConverter extends AbstractArrayConverter {

    public function convert() {
        $result = [];
        foreach($this->input as $key => $value) {

            $sub_keys = explode($this->separator, $key);
            $intermediate = &$result;
            foreach($sub_keys as $sub_key) {
                if (!isset($intermediate[$sub_key])) {
                    $intermediate[$sub_key] = [];
                }
                $intermediate = &$intermediate[$sub_key];
            }
            $intermediate = $value;

        }
        return $result;
    }

}
