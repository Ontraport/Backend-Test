package com.xocevad.engineering.skills;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.LinkedHashMap;
import java.util.Map;

import com.google.gson.JsonParser;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonPrimitive;

import org.junit.jupiter.api.Test;
import org.opentest4j.AssertionFailedError;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.fail;


/**
 * Unit tests of the class Skills implementing functions specified by ONTRAPORT's online
 * GitHub Backend-Test, here named convertMultiToOne() and convertOneToMulti().
 * 
 * Note: test values (input and expected output) are committed as json text files.  The tests
 * convert these (by way of GSON) to Java containers (maps/arrays).  The class under test,
 * "Skills", deals in such native Java objects, with no awareness of JSON.
 * 
 * Note the files ontraport-deep.json and ontraport-flat.json are the original examples given
 * in the Backend-Test repo README.md (with double-quotes rather than single, making it proper
 * JSON).  I have added several other files, supporting more thorough testing.
 */
public class SkillsTest {

    //--------------------------------------------------------------------------------------------//

    // Test convertMultiToOne(): convert a multi-dimensional hierarchal container to a
    // one-dimensional associative array, whose keys represent paths in the hierarchy.
    @Test
    public void testConvertMultiToOne() throws IOException {
        var input = readHierJsonTextFileToJava("src/test/resources/ontraport-deep.json");
        var expectedOutput = readFlatJsonTextFileToJava("src/test/resources/ontraport-flat.json");
        
        // invoke the method in question
        var output = Skills.convertMultiToOne(input);
        assertTreeEquals(expectedOutput, output);
}
    
    // Observe mismatch of containers when the json file text is similarly mismatched.
    @Test
    public void testConvertMultiToOneNegative() throws IOException {
        var input = readHierJsonTextFileToJava("src/test/resources/ontraport-deep.json");
        // Load a file with slightly different structure than ontraport-flat.json,
        // demonstrate that it does *not* compare equal to the product of
        // convertMultiToOne(ontraport-deep.json).
        var expectedOutput = readFlatJsonTextFileToJava("src/test/resources/negative-flat-1.json");

        // invoke the method in question
        var output = Skills.convertMultiToOne(input);
        assertTreeNotEquals(expectedOutput, output);
        
        // another file slightly mismatched
        expectedOutput = readFlatJsonTextFileToJava("src/test/resources/negative-flat-2.json");
        assertTreeNotEquals(expectedOutput, output);
        
    }
    
    // A more challenging test than testConvertMultiToOne():
    // - The top-most construct of the multi-dimensional container is an array
    //   rather than an object with named members.
    // - The container holds values of heterogeneous types.
    // - Some values are null.
    // - An object has a member named like an integer, making it look like an array index.
    @Test
    public void testConvertMultiToOneChallenging() throws IOException {
        var input = readHierJsonTextFileToJava("src/test/resources/challenge-deep.json");
        var expectedOutput = readFlatJsonTextFileToJava("src/test/resources/challenge-flat.json");
        
        // invoke the method in question
        var output = Skills.convertMultiToOne(input);
        assertTreeEquals(expectedOutput, output);
    }
    
    
    //--------------------------------------------------------------------------------------------//

    // Test the reverse, convertOneToMulti(): convert one-dimensional associative array, whose
    // keys represent paths in a hierarchy, to a multi-dimensional hierarchal container.
    @Test
    public void testConvertOneToMulti() throws IOException {
        var input = readFlatJsonTextFileToJava("src/test/resources/ontraport-flat.json");
        var expectedOutput = readHierJsonTextFileToJava("src/test/resources/ontraport-deep.json");
        
        // invoke the method in question
        var output = Skills.convertOneToMulti(input);
        assertTreeEquals(expectedOutput, output);
    }
    
    // Observe mismatch of containers when the json file text is similarly mismatched.
    @Test
    public void testConvertOneToMultiNegative() throws IOException {
        var input = readFlatJsonTextFileToJava("src/test/resources/ontraport-flat.json");
        var expectedOutput = readHierJsonTextFileToJava("src/test/resources/negative-deep-1.json");
        
        // invoke the method in question
        var output = Skills.convertOneToMulti(input);
        assertTreeNotEquals(expectedOutput, output);

        // another file slightly mismatched
        expectedOutput = readFlatJsonTextFileToJava("src/test/resources/negative-deep-2.json");
        assertTreeNotEquals(expectedOutput, output);
    }
    
    // A more challenging test than testConvertOneToMulti():
    // - The top-most construct of the multi-dimensional container should be an array
    //   rather than an object with named members.
    // - The container holds values of heterogeneous types.
    // - Some values are null.
    // - An object has a member named like an integer, making it look like an array index.
    @Test
    public void testConvertOneToMultiChallenging() throws IOException {
        var input = readFlatJsonTextFileToJava("src/test/resources/challenge-flat.json");
        var expectedOutput = readHierJsonTextFileToJava("src/test/resources/challenge-deep.json");
        
        // invoke the method in question
        var output = Skills.convertOneToMulti(input);
        assertTreeEquals(expectedOutput, output);
    }
    
    //--------------------------------------------------------------------------------------------//
    // supporting utilities
    
    JsonElement readJsonTextFile(String filePath) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(filePath)));
        return JsonParser.parseString(content);
    }
    
    // Read hierarchical, i.e. multi-dimensional
    Object readHierJsonTextFileToJava(String filePath) throws IOException {
        var element = readJsonTextFile(filePath);
        return jsonToJava(element);
    }
    
    // Read flat, i.e. one-dimensional
    Map<String, Object> readFlatJsonTextFileToJava(String filePath) throws IOException {
        var element = readJsonTextFile(filePath);
        return jsonToJava(element.getAsJsonObject());
    }
    
    private static Object jsonToJava(JsonElement json) {
        if (json.isJsonObject()) {
            return jsonToJava(json.getAsJsonObject());
        
        } else if (json.isJsonArray()) {
            return jsonToJava(json.getAsJsonArray());
        
        } else if (json.isJsonPrimitive()) {
            return jsonToJava(json.getAsJsonPrimitive());
        
        } else if (json.isJsonNull()) {
            return null;
        
        } else {
            // should never happen
            throw new RuntimeException("unexpected type in JsonElement");
        }
    }
    
    private static Map<String, Object> jsonToJava(JsonObject json) {
        // has members: key-value pairs, key=String, value=JsonElement
        var map = new LinkedHashMap<String, Object>();
        for (var entry : json.entrySet()) {
            map.put(entry.getKey(), jsonToJava(entry.getValue()));
        }
        return map;
    }
    
    private static Object[] jsonToJava(JsonArray json) {
        // unnamed members
        var nElements = json.size();
        var array = new Object[nElements];
        for (int n = 0; n < nElements; ++n) {
            array[n] = jsonToJava(json.get(n));
        }
        return array;
    }
    
    private static Object jsonToJava(JsonPrimitive json) {
        if (json.isBoolean()) {
            return Boolean.valueOf(json.getAsBoolean());
        } else if (json.isNumber()) {
            return jsonToBoxedNumeric(json);
        } else if (json.isString()) {
            return json.getAsString();
        } else {
            throw new RuntimeException("unexpected type in JsonPrimitive");
        }
    }
    
    private static Object jsonToBoxedNumeric(JsonPrimitive json) throws NumberFormatException {
        try {
            long l = json.getAsLong();
            double dl = (double)l;
            double d = json.getAsDouble();
            if (d != dl) {
                // getAsLong() performed rounding, so prefer Double value.
                return Double.valueOf(d);
            }
            // fractional part is 0 so prefer integral type to avoid serializing with ".0"
            return Long.valueOf(l);
        
        } catch (NumberFormatException ignored) {
            // getAsLong() threw: the value contained is not a valid long
        }

        return Double.valueOf(json.getAsDouble());
    }

    //--------------------------------------------------------------------------------------------//

    void assertTreeEquals(Object expected, Object actual) {
        if (expected == null) {
            assertEquals(expected, actual);
        } else if (expected instanceof Map) {
            assertMapEquals((Map<?,?>)expected, (Map<?,?>)actual);
        } else if (expected.getClass().isArray()) {
            assertArrayEquals((Object[])expected, (Object[])actual);
        } else {
            assertEquals(expected, actual);
        }
    }
    
    void assertTreeNotEquals(Object unexpected, Object actual) {
        try {
            assertTreeEquals((Map<?,?>)unexpected, (Map<?,?>)actual);
            // if it didn't fail, they are equal, contrary to this method's assertion.
            fail(String.format("unexpected: %s but got equal: %s", unexpected, actual));
        } catch (AssertionFailedError e) {
            // nothing to do: args are not equal, as asserted.
        }
    }
    
    void assertMapEquals(Map<?,?> expected, Map<?,?> actual) {
        assertEquals(expected.size(), actual.size());
        var iterActual = actual.entrySet().iterator();
        for (var expectedEntry : expected.entrySet()) {
            var actualEntry = iterActual.next();
            assertEquals(expectedEntry.getKey(), actualEntry.getKey());
            assertTreeEquals(expectedEntry.getValue(), actualEntry.getValue());
        }
    }
    
    void assertArrayEquals(Object[] expected, Object[] actual) {
        var length = expected.length;
        assertEquals(length, actual.length);
        for (int n = 0; n < length; ++n) {
            assertTreeEquals(expected[n], actual[n]);
        }
    }

}
