import static org.junit.jupiter.api.Assertions.*;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

class TestContainerConverter {
	
	/* Test for turning a multidimension container into a single dimension one*/
	@Test
	void testToSingleExample() {
		JSONObject start = new JSONObject();
		JSONObject one = new JSONObject();
		JSONObject eight = new JSONObject();
		JSONObject nine = new JSONObject();
		JSONArray four = new JSONArray();
		JSONObject result;
		
		// setup the original container
		four.put(5);
		four.put(6);
		four.put(7);
		
		one.put("two", 3);
		one.put("four", four);
		
		nine.put("ten", 11);
		
		eight.put("nine", nine);
		
		start.put("one", one);
		start.put("eight", eight);
		
		result = ContainerConverter.toSingleDimension(start);
		
		// check that all keys were created properly
		assertEquals(5, result.length());
		assert(result.has("one/two"));
		assert(result.has("one/four/0"));
		assert(result.has("one/four/1"));
		assert(result.has("one/four/2"));
		assert(result.has("eight/nine/ten"));
		
		//check that values are correct and assigned to correct keys
		assertEquals(3, result.get("one/two"));
		assertEquals(5, result.get("one/four/0"));
		assertEquals(6, result.get("one/four/1"));
		assertEquals(7, result.get("one/four/2"));
		assertEquals(11, result.get("eight/nine/ten"));
	}

	/* Test for turning a single dimension container into a multidimension one */
	@Test
	void testToMultiExample() {
		JSONObject start = new JSONObject();
		JSONObject result;
		
		// setup the original container
		start.put("eight/nine/ten", 11);
		start.put("one/four/0", 5);
		start.put("one/two", 3);
		start.put("one/four/1", 6);
		start.put("one/four/2", 7);
		
		result = ContainerConverter.toMultiDimension(start);
		
		// check that 1st level keys were created properly
		assertEquals(2, result.length());
		assert(result.has("one"));
		assert(result.has("eight"));
		
		// check that 1st level values are correct and assigned to correct keys
		assert(result.get("one") instanceof JSONObject);
		assert(result.get("eight") instanceof JSONObject);
		
		//check that 2nd level keys were created properly
		JSONObject one = result.getJSONObject("one");
		JSONObject eight = result.getJSONObject("eight");
		
		assertEquals(2, one.length());
		assertEquals(1, eight.length());
		assert(one.has("two"));
		assert(one.has("four"));
		assert(eight.has("nine"));
		
		//check that 2nd level values are correct and assigned to correct keys
		assertEquals(3, one.get("two"));
		assert(one.get("four") instanceof JSONArray);
		assert(eight.get("nine") instanceof JSONObject);
		assertEquals(5, one.getJSONArray("four").get(0));
		assertEquals(6, one.getJSONArray("four").get(1));
		assertEquals(7, one.getJSONArray("four").get(2));
		
		// check that 3rd level key is created properly
		JSONObject nine = eight.getJSONObject("nine");
		
		assertEquals(1, nine.length());
		assert(nine.has("ten"));
		
		// check that 3rd level value is correct and assigned to correct key
		assertEquals(11, nine.get("ten"));
	}
}
