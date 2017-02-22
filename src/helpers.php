<?php

function debug($x, $exit=false, $var_dump=false) {
	
	echo"<pre class='debug'>\n";
	
	if (is_array($x) || is_object($x)) {
		if ($var_dump) {
			var_dump($x);
		} else {
			print_r($x);
		}
	} else {
		if ($var_dump) {
			var_dump($x);
		} else {
			echo "$x";
		}
	}
	
	echo "</pre>";
	
	if ($exit) {
		exit('DEBUG EXIT');
	}
}

