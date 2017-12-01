function MultiDimensionToOneDimension(input)
{
	for(var inner in input)
	{
		var inner2 = input[inner];
		if(inner2 instanceof Object)
		{
			addToChar += inner +'/';
			MultiDimensionToOneDimension(inner2);
		}
		else
		{
			output[addToChar + inner] =  inner2;
		}
	}
};

var input = {
	    'one' : {
	        'two' : 3,
	        'four' : [ 5,6,7]
	    },
	    'eight' : {
	        'nine' : {
	    			'ten' : 11
	        	}
	    }
	};

	var output = {};
	var addToChar = '';

//running the function
MultiDimensionToOneDimension(input);

//test case
for(var inner in output)
{
	alert('\'' + inner + '\'' + ':' +output[inner]);
}

//////////////////////////////



function OneDimensionToMulti(input)
{
	for(keys in input)
		{
		var arr = keys.split('/');
		var tmp = output;

		for (var i=0;i < arr.length -2; i++)
		{
			if(arr[i] in tmp == false)
			{
				tmp[arr[i]]={};
			}
			tmp = tmp[arr[i]];
		}
		
		if(arr[arr.length - 2] in tmp == false)
		{
			tmp[arr[arr.length - 2]] = [];
		}
		tmp[arr[arr.length - 2]].push(input[keys]);
	}
};

var input = {
	    'one/two/0' : 3,
	    'one/four/0' : 5,
	    'one/four/1' : 6,
	    'one/four/2' : 7,
	    'eight/nine/ten/0' : 11  
	};


var output = {};

//running the function
OneDimensionToMulti(input);

//test cases
alert(output['one']['two']);
alert(output['eight']['nine']['ten']);
alert(output['one']['four']);
		
