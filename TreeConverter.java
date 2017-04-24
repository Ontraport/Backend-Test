import java.util.LinkedHashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

// Class to hold individual hash levels in hash tree.  Theoretically, this structure 
// could be used to hold values at middle levels of the tree, although that is not 
// currently implemented.
class HashAndValues {
  public LinkedHashMap<String, HashAndValues> subHashAndValues;  
  public ArrayList<Integer> nodeValues;

  HashAndValues() 
  {
    subHashAndValues = new LinkedHashMap<String, HashAndValues>();
    nodeValues =  new ArrayList<Integer>();
  }
}

public class TreeConverter
{
  public static void main(String[] args)
  {
    // Create a sample set of the flat hash
    LinkedHashMap<String, Integer> flatHash = new LinkedHashMap<String, Integer>();
    flatHash.put("one/two", 3);
    flatHash.put("one/four/0", 5);
    flatHash.put("one/four/1", 6);
    flatHash.put("one/four/2", 7);
    flatHash.put("eight/nine/ten", 11);

    // call method to create deep hash tree from flat hash
    HashAndValues deepHash = hashify(flatHash);

    // call method to flatten deep hash
    flatten(deepHash);
  }

  // Convert a hash tree to a flat hash that holds path=>value key value pairs
  public static LinkedHashMap<String, Integer> flatten(HashAndValues deepHash)
  {
    LinkedHashMap<String, Integer> flatHash = new LinkedHashMap<String, Integer>();
 
    // Call a recursive method to build the individual paths as an array of strings
   ArrayList<String> pathArray = buildPaths(deepHash);
    // convert the full string representation of path/values to a hash where path = key
    for (String path : pathArray) 
    {
      String[] parsedPath = path.split(":::");
      flatHash.put(parsedPath[0], Integer.valueOf(parsedPath[1]));
    }
    return flatHash;
  }

  // Recursive method to build a string array of all unique paths to node values.  Each
  // string is delimited as path_string:::value.
  public static ArrayList<String> buildPaths(HashAndValues deepHash) 
  {
    ArrayList<String> pathArray = new ArrayList<String>();

    // process each sub hash in the provided hash
    for (String key : deepHash.subHashAndValues.keySet()) {
      // recursively call this method to buid paths for the next hash level
      ArrayList<String> subPathArray = buildPaths(deepHash.subHashAndValues.get(key));
      if (subPathArray.isEmpty()) {
        // this is an end node.  Grab the leaf values. If there is only one end value, simply
        // add it to the current key.  If there are mulitple leaf values, create a path entry
        // for each value. 
        ArrayList<Integer> valueArray = deepHash.subHashAndValues.get(key).nodeValues;
        if (valueArray.size() == 1)
        {
          pathArray.add(key + ":::" + valueArray.get(0));
        } else {
          for (int i = 0; i < valueArray.size(); i++) {
            pathArray.add(key + "/" + i + ":::" + valueArray.get(i));
          }
        }
      } else {
        // this is an internediate level in the path.  Add an entry for this level and every sub
        // level returned from recursive calls.
        for (String subPath : subPathArray) 
        {
          pathArray.add(key + "/" + subPath);
        }
      }
    }

    return pathArray;
  }

  // create a deep hash tree from a flat hash of paths
  public static HashAndValues hashify(LinkedHashMap<String, Integer> flatHash)
  {
    HashAndValues deepHash = new HashAndValues();
    // process all path / value entries in flatHash
    for (String key : flatHash.keySet()) {
      int thisValue = flatHash.get(key);
      String[] keyParts = key.split("/");
      
      // if the last value is an integer, this is part of an array of nodeValues
      boolean holdsArrayValue = true;
      try
      {
        Integer.parseInt(keyParts[keyParts.length - 1]);
      }
      catch (NumberFormatException nfe) {
        holdsArrayValue = false;
      }

      // Set the curr hash to the first hash node sub hash
      LinkedHashMap<String, HashAndValues> prevHashAndValues = null;
      LinkedHashMap<String, HashAndValues> currHashAndValues = deepHash.subHashAndValues;
      // process all but the last element of path
      for(int i = 0; i < keyParts.length - 1; i++)
      {
        // if there is not a hash key yet, create one
        if (currHashAndValues.get(keyParts[i]) == null) 
        {
          currHashAndValues.put(keyParts[i], new HashAndValues());
        }
        // set the curr hash to the new sub hash 
        prevHashAndValues = currHashAndValues;
        currHashAndValues = currHashAndValues.get(keyParts[i]).subHashAndValues;
      }
      if (holdsArrayValue) {
        // this path holds an array value.  Add the value to the existing level's array and ignore
        // the number key in the path
        prevHashAndValues.get(keyParts[keyParts.length - 2]).nodeValues.add(thisValue);
      } else {
        // this path holds a single value.  Add the current key to the path and add the value.
        currHashAndValues.put(keyParts[keyParts.length - 1], new HashAndValues());
        currHashAndValues.get(keyParts[keyParts.length - 1]).nodeValues.add(thisValue);
      }
    }
    return deepHash;
  }
}
