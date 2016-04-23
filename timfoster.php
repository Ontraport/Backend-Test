<?php

$mdcontainer = array( 
            "one" => array (
               "two" => 3,
               "four" => array (5,6,7)
            ),
            
            "eight" => array (
               "nine" => array("ten" => array(11))
            )
         );
         
         
echo 'Original: '.print_r($mdcontainer,true);

// {
//     'one/two':3,
//     'one/four/0':5,
//     'one/four/1':6,
//     'one/four/2':7,
//     'eight/nine/ten':11
// }

$singleDimension = array();
$keysArr = array();
$valArr = array();
$reversed = array();


//check if an array
//if array we need to cycle through until we get an end value
//if it is not an array, add to the single dimension array

function buildSingle($array, $parentKey, $key){
	global $singleDimension;
	foreach($array as $key=>$l1value){
		
		if(is_array($l1value)){
			//we need to cycle through array and send back to this function.
				//echo 'Parent Key: '.$parentKey.' Key: '.$key.'<br/>';
				
				if(strlen($parentKey)>0){
					buildSingle($l1value, $parentKey.'/'.$key, $key);
				}
				else {
					buildSingle($l1value, $key, $key);
				}	
		}
		else {
			//we have an end value, add to the single dimension array
			//echo 'xParent Key: '.$parentKey.' Key: '.$key.'<br/>';
				$singleDimension[$parentKey.'/'.$key] = $l1value;
			
			

		}
	
	}
}


function reverseSingle($sdArray){
	global $reversed;
	global $valArr;
	//$tempKey = '';
	$partsCountArray = array();
	
	
	//echo '<br/>To reverse: '.print_r($sdArray,true);
	foreach($sdArray as $key=>$value) {
		$keyArr = explode('/', $key);
		$valArr[] = $value;
		$partsCountArray[$key] = count($keyArr);
	}
	$valArr = array_reverse($valArr);
	$maxLevels = max($partsCountArray);
	//echo '<br/>Parts Array: '.print_r($partsCountArray,true);
	array_multisort($partsCountArray, SORT_DESC,SORT_NUMERIC);
		//echo '<br/>Parts Array: '.print_r($partsCountArray,true);
	$counter = 0;	
	foreach($partsCountArray as $key=>$value) {
		$parts = $value;
		//echo '<br/>Parts: '.$value;
		//echo '<br/>Key: '.$key;
		$keyArr = explode('/', $key);
		$i = $parts-1;
		$x = 1;
		$j = 0;
		$tempArr = array();
		

		while ($i >= 0) {
			$j = $i + 1;
				if($x <= 1){
					$tempArr[$keyArr[$i]] = $valArr[$counter];			  
				}
				else {				
					$tempArr[$keyArr[$i]] = array();			  
				}
			$x++;
			$i--;  
		}
			//echo '<br/>Temp: '.print_r($tempArr,true);
			$counterTwo = 1;
		foreach ($tempArr as $key=>$value){
		//echo '<br/>'.$key.' '.$value;
			if($counterTwo <= 1){
				$array = array($key => $value);	
			}
			else {
      			$array = array($key => $array);
      		}
      		$counterTwo = $counterTwo + 1;
      	}
      
		//echo '<br/>Temp Newm: '.print_r($array,true);
		$reversed = array_replace_recursive($reversed, $array);
		$array = null;
		$counter = $counter + 1;	
	}
}




//multiToAssoc($mdcontainer);
buildSingle($mdcontainer);
echo '<br/><br/>Single Dimension: '.print_r($singleDimension, true);
reverseSingle($singleDimension);
$reversed = array_reverse($reversed);
echo '<br/><br/>Reversed: '.print_r($reversed, true);
//echo '<br/>'.print_r($valArr, true);

?>