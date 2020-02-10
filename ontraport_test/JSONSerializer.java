
/*
 * Author: Richard Manson-Hing
 * Date: 2/6/2020
 * 
 * Comment: RE: application for ONTRAPORT Backend Job Position
 * 
 * Assumptions:
 * arrays can only store "scalar" values like int, long and "not strictly speaking a scalar String" NOT arrays or Objects
 * ie arrays only occur at the end of the path
 * probably could fix this restriction to allow arrays and objects to hold anything!
 * but the cost may be more complexity!
 * 
 */


import java.util.*;
import org.json.*;


public class JSONSerializer {
	

	public static JSONObject OutputJSON = new JSONObject();
	public static JSONObject ExpandedJSON = new JSONObject();
	
	public JSONSerializer() {
		
	}
	
	
	public void recurseObject(String path, JSONObject obj) {
		Iterator<String> keys = obj.keys();
		
		while (keys.hasNext()) {
			String key = keys.next();
			
			if(obj.get(key) instanceof Integer) {
				if(path.equals("")) {
					OutputJSON.put(key, ((Integer)obj.get(key)).intValue());
				} else {
					OutputJSON.put(path + "/" + key, ((Integer)obj.get(key)).intValue());
				}
			} else if(obj.get(key) instanceof Long) {
				if(path.equals("")) {
					OutputJSON.put(key, ((Long)obj.get(key)).longValue());
				} else {
					OutputJSON.put(path + "/" + key, ((Long)obj.get(key)).longValue());
				}
			}else if(obj.get(key) instanceof String) {
				if(path.equals("")) {
					OutputJSON.put(key, (String)obj.get(key));
				} else {
					OutputJSON.put(path + "/" + key, (String)obj.get(key));
				}
			} else if(obj.get(key) instanceof JSONObject) {
				if(path.equals("")) {
					recurseObject(key, (JSONObject)obj.get(key));
				} else {
					recurseObject(path + "/" + key, (JSONObject)obj.get(key));
				}
			} else if(obj.get(key) instanceof JSONArray) {
				if(path.equals("")) {
					recurseArray(key, (JSONArray)obj.get(key));
				} else {
					recurseArray(path + "/" + key, (JSONArray)obj.get(key));
				}	
			}
			
		}
		
		
		return;
	}
	
	public void recurseArray(String path, JSONArray arr) {
		int arrayLength = arr.length();
		int x = 0;
		
		for(x=0; x<arrayLength; x++) {
			if(arr.get(x) instanceof Integer) {
				if(path.equals("")) {
					OutputJSON.put(String.valueOf(x), ((Integer)arr.get(x)).intValue());
				} else {
					OutputJSON.put(path + "/" + String.valueOf(x), ((Integer)arr.get(x)).intValue());
				}
			} else if(arr.get(x) instanceof Long) {
				if(path.equals("")) {
					OutputJSON.put(String.valueOf(x), ((Long)arr.get(x)).longValue());
				} else {
					OutputJSON.put(path + "/" + String.valueOf(x), ((Long)arr.get(x)).longValue());
				}
			} else if(arr.get(x) instanceof String) {
				if(path.equals("")) {
					OutputJSON.put(String.valueOf(x), (String)arr.get(x));
				} else {
					OutputJSON.put(path + "/" + String.valueOf(x), (String)arr.get(x));
				}
			} else if(arr.get(x) instanceof JSONObject) {
				recurseObject("", (JSONObject)arr.get(x));
			} else if(arr.get(x) instanceof JSONArray) {
				recurseArray("", (JSONArray)arr.get(x));
			}
		}
		
		return;
	}
	
	
	
	public void expandPathsIntoJSONObject(JSONObject rootObject) {
		Iterator<String> keys = rootObject.keys();
		
		while (keys.hasNext()) {
			String key = keys.next();
			Object valueObject = rootObject.get(key);
			
			String[] pathTokenArray = key.split("/");
			int arrayLength = pathTokenArray.length;
			
			if (isInteger(pathTokenArray[arrayLength-1])) {
				recursePathToArray(ExpandedJSON, key, valueObject);
			} else {
				recursePathToScalar(ExpandedJSON, key, valueObject);
			}	
		}	
	}
	
	
	
	public void recursePathToScalar(JSONObject currentObject, String pathToScalar, Object valueObject) {
		String[] pathTokenArray = pathToScalar.split("/");
	    int arrayLength = pathTokenArray.length;
	    
	    if (arrayLength == 1) {
	        	currentObject.put(pathTokenArray[0], valueObject);
	    } else if (arrayLength > 1) {
	    		if (currentObject.has(pathTokenArray[0])) {
	    			Object foundObject = currentObject.get(pathTokenArray[0]);
	    			if(foundObject instanceof JSONObject) {
			    	    String newPathToScalar = pathToScalar.replaceFirst("\\w+/", "");
		    			recursePathToScalar((JSONObject)foundObject, newPathToScalar, valueObject);
	    			}
	    		} else {
		    	    JSONObject newObj = new JSONObject();
		    	    currentObject.put(pathTokenArray[0], newObj);
		    	    String newPathToScalar = pathToScalar.replaceFirst("\\w+/", "");
		    	    recursePathToScalar(newObj, newPathToScalar, valueObject);
	    		}
	    	

	    }
	}
	
	
	
	public void recursePathToArray(JSONObject currentObject, String pathToArray, Object valueObject) {
		String[] pathTokenArray = pathToArray.split("/");
		int arrayLength = pathTokenArray.length;
	    
	    if (arrayLength == 2) {
	    		int arrayIndex; 
		    try {
		    	    arrayIndex = Integer.parseInt(pathTokenArray[1]);
		    	    
		    	    if (currentObject.has(pathTokenArray[0])) {
		    	        	Object foundObject = currentObject.get(pathTokenArray[0]);
		    	        	if(foundObject instanceof JSONArray) {
		    	        		((JSONArray)foundObject).put(arrayIndex, valueObject);
		    	        	}
		    	    } else {
			    		JSONArray arrayOfValues = new JSONArray();
			    		arrayOfValues.put(arrayIndex, valueObject);
			    		currentObject.put(pathTokenArray[0], arrayOfValues);
		    	    }
		    } catch ( NumberFormatException e) {
		    		return;
		    }
	    } else if (arrayLength > 2) {
		    	if (currentObject.has(pathTokenArray[0])) {
		    		Object foundObject = currentObject.get(pathTokenArray[0]);
		    		if(foundObject instanceof JSONObject) {
		    			String newPathToArray = pathToArray.replaceFirst("\\w+/", "");
			    	    recursePathToArray((JSONObject)foundObject, newPathToArray, valueObject);
		    		}
		    	} else {
		    	    JSONObject newObj = new JSONObject();
		    	    currentObject.put(pathTokenArray[0], newObj);
		    	    String newPathToArray = pathToArray.replaceFirst("\\w+/", "");
		    	    recursePathToArray(newObj, newPathToArray, valueObject);
		    	}
	    }   
	}
	
	
	public boolean isInteger(String input) {
	    try {
	        Integer.parseInt(input);
	        return true;
	    }
	    catch ( NumberFormatException e) {
	        return false;
	    }
	}
	
	
	public static void main(String[] args) {
		
		//Use this data to test integers and arrays of integers
		String inputJSONString = "{\n" + 
				"    'one':\n" + 
				"    {\n" + 
				"        'two': 3,\n" + 
				"        'four': [ 5,6,7]\n" + 
				"    },\n" + 
				"    'eight':\n" + 
				"    {\n" + 
				"        'nine':\n" + 
				"        {\n" + 
				"            'ten':11\n" + 
				"        }\n" + 
				"    }\n" + 
				"}";
		
		
		/*
		//Use this data to test strings
		String inputJSONString = "{\n" + 
				"    'one':\n" + 
				"    {\n" + 
				"        'two': 'Z',\n" + 
				"        'four': ['a', 'b', 'c']\n" + 
				"    },\n" + 
				"    'eight':\n" + 
				"    {\n" + 
				"        'nine':\n" + 
				"        {\n" + 
				"            'ten':'ZZ'\n" + 
				"        }\n" + 
				"    }\n" + 
				"}";
		*/
		
		//print the original multi-dimensional container as a string
		System.out.println("\n" + "THE ORIGINAL MULTI-DIMENSIONAL CONTAINER");
		System.out.println(inputJSONString + "\n");
		
		//import the json string intoJSONObject
		JSONObject jsonStringAsJSONObject = new JSONObject(inputJSONString); 
		
		//print the JSONObject to string
		//System.out.println(jsonStringAsJSONObject.toString(5));
		
		JSONSerializer serializer = new JSONSerializer();
		OutputJSON = new JSONObject();
		
		//start recursing through the input JSONObject and creating slash delimited paths in output global object OutputJSON
		serializer.recurseObject("", jsonStringAsJSONObject);
		
		//print the resulting JSONObject we get after creating the slash delimited paths
		//THIS IS PART 1 of exercise completed
		System.out.println("RESULT OF PART 1 OF THE BACKEND TEST");
		System.out.println(OutputJSON.toString(5) + "\n");
		
		//Now do the reverse - convert slash delimited paths to original input json
		ExpandedJSON = new JSONObject();
		serializer.expandPathsIntoJSONObject(OutputJSON);
		
		//THIS IS PART 2 of exercise completed
		System.out.println("RESULT OF PART 2 OF THE BACKEND TEST");
		System.out.println(ExpandedJSON.toString(5) + "\n");
	}
	
	
	
	
}  //end class JSONSerializer