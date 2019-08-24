function toAssociativeArray(currentObj, path, finalObj) {
	//This function pertains to question 1.
  //Takes in multidimensional object 'currentObj'.
  //Initially, path = '' and finalObj = {}.
  //After completion, finalObj will be the desired associative array.

  if (typeof(currentObj) !== "object") {
		finalObj[path] = currentObj;
  }
  //recursively call on each key w/ corresponding path
  for (let key in currentObj) {
    toAssociativeArray(currentObj[key], path + '/' + key, finalObj);
  }
}

function fromAssociativeArray(currentObj, finalObj) {
	//This function pertains to question 2.
	//Takes in associative array currentObj.
  //Initially, finalObj = {}.
  //After completion, finalObj will be the desired multi-dimensional object.

	let newObj = {};
  let i = 0;
  for (let key in currentObj){
  	//parse the path for easier handling
  	newObj[i] = JSON.parse(JSON.stringify(key)).split("/");

    //create reference for use in next for loop
  	var finalCopy = finalObj;

  	for(var j = 1; j < (newObj[i]).length; j++){

  		if (typeof(finalCopy[newObj[i][j]]) == 'undefined'){
  			finalCopy[newObj[i][j]] = {};
  		}
  		else{
    		//do nothing (key/directory already exists)
  		}
    	if (j < (newObj[i]).length-1){
      	finalCopy = finalCopy[newObj[i][j]];
    	}
    	else{
      	finalCopy[newObj[i][j]] = currentObj[key];
    	}
  	}
  	i++;
	}
}

//Object used in testing
let nestedObj = {
	'one':
  {
  'four': [5, 6, 7],
  	'two': 3
  },
  'eight':
    {
    'nine':
    {
  		'ten': 11
  	}
  }
};
let path = '';
let finalObj1 = {};

//test first function
toAssociativeArray(nestedObj, path, finalObj1);
console.dir(finalObj1);

//copy result, for input to second function
let newObj = JSON.parse(JSON.stringify(finalObj1));
let finalObj2 = {};

//test second function
fromAssociativeArray(newObj, finalObj2);
console.dir(finalObj2);

alert("Success");
