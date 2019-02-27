import java.util.Iterator;
import java.util.Stack;

import com.google.gson.*;

public class main {

    /* This is my submission for the Backend Engineer position. This class requires the Gson library from Google in order to work correctly.
     * Although the assessment description didn't explicitly state it, I assumed from looking at the sample input and output that the data structures were JSON.
     *
     * main() sets up a string "input" where JSON strings will be placed. Then feeds this input string to compressFunction() which will fulfill question #1.
     * Output will be printed to console.
     * The output of compressFunction() will then be fed to expandFunction() which will fulfill question #2. Output will be printed to console.
     *
     * These 2 functions can handle nested JsonObjects, nested JsonArrays, or a combination of both. They can also ensure array order.
     * One edge case that will cause my functions to break is if the top level JsonElement is a JsonArray.
     * */

    //JsonObject that represents the 1-Dim array with keys as string paths to values. End result of compressFunction.
    private static JsonObject compressedList = new JsonObject();
    //JsonObject that represents the multi-Dim container with key-value pairs. End result of expandFunction
    private static JsonObject expandedList = new JsonObject();

    public static Gson gson;

    public static void main(String[] args) {
        System.out.println("Beginning program");
        System.out.println();
        gson = new GsonBuilder().setPrettyPrinting().create();

        //Here is where Json string input is set. To test against different JSON strings, set the text here.
        String input = "{\n" +
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

        JsonObject sample = gson.fromJson( input, JsonObject.class);

        //Question #1 Calling the compressFunction
        compressFunction(sample, "");
        System.out.println("Here is the compressed 1-dimensional list: ");
        System.out.println(gson.toJson(compressedList));

        //Question #2 Calling the expandFunction
        expandFunction(compressedList);
        //expandFunction(sample); //comment the line above and run this expandFunction to test directly with the JsonObject "sample"
        System.out.println("Here is the expanded multi-dimensional list: ");
        System.out.println(gson.toJson(expandedList));
    }

    /*Question #1 Function - Takes a JsonObject and recursively searches all keys until primitive values are found.
     * Then inserts them in to 1-dim JsonObject    */
    public static void compressFunction(JsonObject jObj, String keyPath)
    {
        Iterator<String> keyIterator = jObj.keySet().iterator();

        while(keyIterator.hasNext())
        {
            String keyName = keyIterator.next();
            JsonElement value = jObj.get(keyName);
            if(value.isJsonObject()) //case 1, the value is a JsonObject. Need to search that object for primitive values
                compressFunction(value.getAsJsonObject(), appendKeyNames(keyPath, keyName));
            else if(value.isJsonArray()) //case 2, the value is a JsonArray. Need to search that array for primitive values
            {
                JsonArray jArray = value.getAsJsonArray();
                for(Integer i = 0, s = jArray.size(); i < s; i++)
                {
                    JsonObject arrayElement = new JsonObject();
                    arrayElement.add(i.toString() , jArray.get(i));
                    compressFunction(arrayElement, appendKeyNames(keyPath, keyName));
                }
            }
            else if(value.isJsonPrimitive() || value.isJsonNull()) //case 3, simple case where primitive value is found. Just insert keyPath with value.
                compressedList.add(appendKeyNames(keyPath, keyName), value);
        }
    }

    //helper function to make code less verbose. Appends keyNames together with a / in between, but only if the first string is not null.
    private static String appendKeyNames(String keyPath, String keyName)
    {
        if(keyPath.isEmpty())
            return keyName;
        else
            return keyPath + "/" + keyName;
    }

    /*Question #2 Function - This function does the reverse of compressFunction. Takes a JsonObject representing a
     * 1-dim array with keys as paths to values, and expands it.
     * Contains 2 parts.
     * First part expandFunction(), does expansion but treats JsonArrays as JsonObjects. Creates a JsonObject keys as index numbers and associated values.
     * Second Part orderArrays(), does a second pass over the semi-expanded JsonObject and detects if a JsonObject is actually a stand-in
     * for a JsonArray, by looking at the key strings. If all the strings are numeric, aka [1234567890], then its a stand-in.
     * Then replaces that JsonObject with a JsonArray that has all of the same values, in the correct order as specified by the key strings as index placements*/
    public static void expandFunction(JsonObject jObj /*jObj is the 1-dim array that will need to be expanded*/)
    {
        Iterator<String> keyIterator = jObj.keySet().iterator();

        while(keyIterator.hasNext())
        {
            String keyPath = keyIterator.next();
            String[] keyPathSplit = keyPath.split("/");
            JsonElement head = expandedList; //expanded list will be the result of this function. Gets traversed as a linked tree list

            //if the key path just has 1 keyname in it, just skip to insertion of the value.
            if(keyPathSplit.length > 1)
            {
                //start iterating at the 2nd keyname if there is one. Look back 1 keyname to see what keyname needs to be added.
                for(int i = 1; i < keyPathSplit.length; i++)
                {
                    //determine if keyname back 1 in path already exists in the current Json structure. if it does traverse to head to that JsonElement. If not
                    // then insert a new json object value with a keyname, in to the current JsonObject pointed to by head.
                    if(head.isJsonObject() && head.getAsJsonObject().has(keyPathSplit[i-1]))
                        head = head.getAsJsonObject().get(keyPathSplit[i-1]);
                    else
                        head = addKeyValuePair(head, keyPathSplit[i-1], new JsonObject()); //add Json Object structure
                }
            }

            //insert a single key-value pair
            addKeyValuePair(head, keyPathSplit[keyPathSplit.length-1], jObj.get(keyPath));
        }

        //System.out.println(gson.toJson(expandedList));
        orderArrays(expandedList, null, "");
    }

    //Traverses through the JsonObject and finds JsonObjects that have keys that are all numbers. Convert them to JsonArrays. Ensures proper order for array elements.
    private static void orderArrays(JsonObject jObj, JsonElement prevElement, String previousKey)
    {
        Iterator<String> keyIterator = jObj.keySet().iterator();
        /* keeps track of which JsonElement we are currently working on and is actually in our Json structure. used for checking which jsonObject to go to after the current one. */
        JsonElement traverseElement =  jObj;
        int i = 0;

        //first, loop needs to determine if jObj needs to be converted to a JsonArray. Loops through all keys to see if any of them are not [1234567890]. If so, can't be converted to a jArray with ordering
        while(keyIterator.hasNext())
        {
            if(!keyIterator.next().replaceAll("[1234567890]", "").isEmpty())
                i++;
        }

        // check if any keynames were found that were not [1234567890]. i represents the count of non-number keys that exist.
        if(i == 0)
        {
            //create new JsonArray and fill it in proper order with JsonElements
            JsonArray jArray = new JsonArray();
            for(int n = 0; jObj.has(n + ""); n++)
                jArray.add(jObj.get(n + ""));

            //replace jObj in previous JsonElement with jArray.
            if(prevElement.isJsonObject())
            {
                prevElement.getAsJsonObject().add(previousKey, jArray);
                traverseElement = prevElement.getAsJsonObject().get(previousKey);
            }
            else
            {
                prevElement.getAsJsonArray().set(Integer.parseInt(previousKey), jArray);
                traverseElement = prevElement.getAsJsonArray().get(Integer.parseInt(previousKey));
            }
        }

        //loop through and recursive call this function on the children. Only if child key-value pair resolves to a JsonObject.
        if(traverseElement.isJsonObject())
        {
            keyIterator = traverseElement.getAsJsonObject().keySet().iterator();
            while(keyIterator.hasNext())
            {
                String keyName = keyIterator.next();
                if(traverseElement.getAsJsonObject().get(keyName).isJsonObject()) //check if child value is JsonObject
                    orderArrays(traverseElement.getAsJsonObject().getAsJsonObject(keyName), traverseElement, keyName);
            }
        }
        else
        {
            for(int x = 0; x < traverseElement.getAsJsonArray().size(); x++)
            {
                if(traverseElement.getAsJsonArray().get(x).isJsonObject()) //check if child value is JsonObject
                    orderArrays(traverseElement.getAsJsonArray().get(x).getAsJsonObject(), traverseElement, x + "");
            }
        }
    }

    //helper function - adds a JsonElement as a value to another JsonElement.
    private static JsonElement addKeyValuePair(JsonElement jEle, String key, JsonElement value)
    {
        if(jEle.isJsonArray())
            jEle.getAsJsonArray().add(value);
        else if(jEle.isJsonObject())
            jEle.getAsJsonObject().add(key, value);

        return value;
    }
}
