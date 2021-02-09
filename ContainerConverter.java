import org.json.JSONObject;
import org.json.JSONArray;
import java.util.*;

public class ContainerConverter {

	/* 
	 * Purpose: Take a multidimensional container and convert it into a single
	 *          dimension container.
	 */
	public static JSONObject toSingleDimension(JSONObject container) {
		JSONObject oneDContainer = new JSONObject(); // the converted container
		
		recurse(oneDContainer, container, "");
		return oneDContainer;
	}
	
	/* 
	 * Purpose: Traverse the multidimensional container, build the various paths,
	 *          and pair them with their respective values
	 */
	private static void recurse(JSONObject oneDContainer, JSONObject jsonObject, String prefix) {
		Iterator<String> keys = jsonObject.keys();
		
		while(keys.hasNext()) {
			String key = keys.next();
			// Continue down the branch if value is another object
			if(jsonObject.get(key) instanceof JSONObject) {
				recurse(oneDContainer, (JSONObject)jsonObject.get(key), prefix+"/"+key);
			} else { 
				// Continue to elements if value is an array
				if(jsonObject.get(key) instanceof JSONArray) {
					handleArray(oneDContainer, jsonObject.getJSONArray(key), prefix+"/"+key);
				} 
				// Add final key string and value to the 1D container
				else {
					oneDContainer.put(prefix.substring(1)+"/"+key, jsonObject.get(key)); // substr to remove first "/"
				}
			}
		}
	}
	
	/* 
	 * Purpose: Handle the base case for traversing in which the value is an array instead of
	 *          a single element. Used by function 'recurse'.
	 */
	private static void handleArray(JSONObject oneDContainer, JSONArray jsonArray, String prefix) {
		String correctedPrefix = prefix.substring(1) + "/"; // remove first "/" and add final one
		for(int i=0; i<jsonArray.length(); i++) {
			oneDContainer.put(correctedPrefix+i, jsonArray.get(i)); 
		}
	}

	/*
	 * Purpose: Take a single dimensional container and turn it into a multidimensional container.
	 */
	public static JSONObject toMultiDimension(JSONObject oneDContainer) {
		JSONObject multiDContainer = new JSONObject(); // the converted container
		Iterator<String> paths = oneDContainer.keys();
		
		// go through all of the key paths
		while(paths.hasNext() ) {
			String path = paths.next();
			String[] keyAndSubpath = getFirstKey(path);
			createObjectFromPath(oneDContainer, multiDContainer, path, keyAndSubpath);
			
		}
		
		return multiDContainer;
	}
	
	/*
	 * Purpose: Take a path key string and create a new or append to an existing multidimensional container based
	 *          off of it.
	 */
	private static void createObjectFromPath(JSONObject originalContainer, JSONObject object, String originalPath, String[] keyAndSubpath) {
		// create an object with a key and a single element value if we're at the end of the path
		if(keyAndSubpath[1].equals("")) {
			object.put(keyAndSubpath[0], originalContainer.get(originalPath));
		}
		// find/create an object with a key and an array value if we're at the second to the end
		// and the last directory is an index value
		else if(keyAndSubpath[1].matches("\\d+")) {
			JSONArray array;
			if(object.has(keyAndSubpath[0])) {
				array = (JSONArray)object.get(keyAndSubpath[0]);
			} else {
				array = new JSONArray();
				object.put(keyAndSubpath[0], array);
			}
			array.put(originalContainer.get(originalPath));
		}
		// find existing child object or create a new one and continue down
		else {
			if(object.has(keyAndSubpath[0])) {
				createObjectFromPath(originalContainer, object.getJSONObject(keyAndSubpath[0]), 
									 originalPath, getFirstKey(keyAndSubpath[1]));
			} else {
				JSONObject childObject = new JSONObject();
				createObjectFromPath(originalContainer, childObject, 
						 			 originalPath, getFirstKey(keyAndSubpath[1]));
				object.put(keyAndSubpath[0], childObject);
			}
		}
	}
	
	private static String[] getFirstKey(String path) {
		String[] result = {path, ""}; 
		
		// get the first key from the path
		for(int i=0; i<path.length()-1; i++) {
			if(path.charAt(i+1) == '/') {
				result[0] = path.substring(0, i+1);
				result[1] = path.substring(i+2);
				break;
			}
		}
		
		return result;
	}
}
