<?php

class OneDimensionArrayConverter extends AbstractArrayConverter {

    public function convert() {
        $result = [];
        $this->run($this->input, $result);
        return $result;
    }

    protected function run($input, &$result, &$input_key = '') {

        foreach($input as $key => $value) {

            $result_key = "{$input_key}{$this->separator}{$key}";

            if (is_array($value)) {
                // dive deeper
                $this->run($value, $result, $result_key);
            } else {
                // cut the separator at the beginning of the key
                $separator_length = strlen($this->separator);
                $result_key = substr($result_key, $separator_length);
                $result[$result_key] = $value;
            }
        }

    }

}
