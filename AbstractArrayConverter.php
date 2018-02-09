<?php


abstract class AbstractArrayConverter {
    const DEFAULT_SEPARATOR = '/';

    abstract public function convert();

    public function __construct(Array $input, $separator = null) {
        $this->input     = $input;
        $this->separator = $separator ?: self::DEFAULT_SEPARATOR;
    }
}
