<?php

class ConverterFactory {
    public static function getConverter($command, $input, $separator) {
        switch($command) {
        case 'multi':
            $instance = new MultiDimensionArrayConverter($input, $separator);
            break;
        case 'one': 
        default:
            $instance = new OneDimensionArrayConverter($input, $separator);
            break;
        }
        return $instance;
    }
}
