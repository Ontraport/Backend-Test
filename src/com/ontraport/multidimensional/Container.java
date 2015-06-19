package com.ontraport.multidimensional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;


public class Container{
	HashMap<String, Object> map;
	
	Container(){
		map = new HashMap<String, Object>();
	}
	
	Container(String key, Object object){
		map = new HashMap<String, Object>();
		map.put(key, object);
	}

	
	public Container add(String key, int... nums){
		ArrayList<Integer> list;
		if(!map.containsKey(key)){
			if(nums.length==1){
				map.put(key, nums[0]);
				return this;
			}
			list = new ArrayList<Integer>();
		}else{
			if(map.get(key) instanceof Integer){
				list = new ArrayList<Integer>();
				list.add((Integer) map.get(key));
			}else{
				list = (ArrayList<Integer>) map.get(key);
			}
		}
		for(int i:nums){
			list.add(i);
		}
		map.put(key, list);
		
		return this;
	}
	
	public Container add(String key, Container c){
		map.put(key, c);
		return this;
	}
	
	public Set<String> getKeys(){
		return map.keySet();
	}
	
	public Object get(String key){
		return map.get(key);
	}
	
	public boolean containsKey(String key){
		return map.containsKey(key);
	}
}