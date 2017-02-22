<?php

header("Content-type: text/plain; charset=utf-8");

require_once('helpers.php');
require_once('example-array.php');

class Pump {
	
	/**
	*
	* "Deflate" a multidimendional array
	* 
	* Reduce a multidimensional array's keys into a
	* flat, slash-delimited key, and append the value.
	*
	* @access public
	* @static
	* @param array $input
	* @return array
	* 
	*/
	
	public static function deflate(array $input) {
		
		$deflated = [];
		
		self::deflate_recursive($deflated, $input);
		
		return $deflated;
		
	}
	
	
	
	/**
	*
	* deflate_recursive
	*
	* Where the magic lives
	*
	* @param array $deflated
	* @param array $input
	* @param scalar $key1
	* @access private
	* @static
	* @return self
	*
	*/
	
	private static function deflate_recursive(array &$deflated, array $input, $key1 = '') {
		
		foreach ($input as $key2 => $value) {
			if (!is_array($value)) {
				$deflated["{$key1}{$key2}"] = $value;
				continue;
			}
			
			self::deflate_recursive($deflated, $value, "{$key1}{$key2}/");
			
		}
	}
	
	
	
	/**
	*
	* "Inflate" or expand a one-dimensional array's keys
	* 
	* Takes an array whose keys are like file paths (a/b/c)
	* and builds them out into child arrays. Once each branch
	* is fully developed, the array's value becomes the leaf.
	* 
	* @param array $input
	*	@access public
	* @static
	* @return array
	*
	*/
	
	public static function inflate(array $input) {
		
		$output = [];
		
		foreach ($input as $key => $val) {
			
			$items = explode('/', $key);
			$value = array_pop($items);
			$parent =& $output;
			
			foreach ($items as $item) {
				if (!isset($parent[$item]) || !is_array($parent[$item])) {
					$parent[$item] = [];
				}
				
				$parent =& $parent[$item];
				
			}
			
			if (empty($parent[$value])) {
				$parent[$value] = $val;
			}
		}
		
		return $output;
		
	}

} // end class
