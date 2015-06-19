package com.ontraport.multidimensional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;
import java.util.TreeSet;

public class Main {
	public static void main(String[] args){
		Container input = new Container("one", new Container("two", 3).add("four", 5, 6, 7)); 
		input.add("eight", new Container("nine", new Container("ten", 11)));
		printContainer(input);
		
		//Q1
		HashMap<String, Integer> map = toArray(input);
		printArray(map);
		
		//Q2
		Container container = toContainer(map);
		printContainer(container);
		
	}
	
	public static Container toContainer(HashMap<String, Integer> array){
		Container container = new Container();
		TreeSet<String> keys = new TreeSet<String>();
		keys.addAll(array.keySet());
		
		//for each element and its single dimensional keys
		for(String key:keys){
			int value = array.get(key);
			String[] strings = key.split("/");
			visitKey(0, strings, value, container);
		}
		
		return container;
	}
	
	
	/*
	 * recursive to visit keys in the array and create a container if it doesn't exist
	 * Put the value into the container if it is the last index
	 */
	public static Container visitKey(int index, String[] strings, int value, Container container){
		if(index==strings.length-1 || strings[index+1].matches("\\d")){
			return container.add(strings[index], value);
		}else{
			if(container.containsKey(strings[index])){
				return visitKey(index+1, strings, value, ((Container)container.get(strings[index])));
			}
			return container.add(strings[index], visitKey(index+1, strings, value, new Container()));
		}
	}
	
	public static HashMap<String, Integer> toArray(Container container){
		HashMap<String, Integer> map = new HashMap<String, Integer>();
		StringBuilder builder = new StringBuilder();
		visitContainer(container, builder, map);
		return map;
	}
	
	/*
	 * Recursive func to visit the nested container and pass on the StringBuilder to create the single dimensional key
	 * Put the key and value if the containing object is not a container (Integer or list of Integers)
	 */
	public static void visitContainer(Container c, StringBuilder builder, HashMap<String, Integer> map){
		Set<String> keys = c.getKeys();
		for(String k:keys){
			builder.append(k);
			Object o = c.get(k);
			if(o instanceof Container){
				builder.append("/");
				visitContainer((Container) o, builder, map);
				builder.deleteCharAt(builder.length()-1);
			}else if(o instanceof Integer){
				map.put(builder.toString(), (Integer) o);
			}else{
				ArrayList<Integer> list = (ArrayList<Integer>) o;
				builder.append("/");
				//value is a list of integers, append the index for each
				for(int i=0; i<list.size(); i++){
					builder.append(i);
					map.put(builder.toString(), list.get(i));
					builder.delete(builder.length()-String.valueOf(list.get(i)).length(), builder.length());
				}
				builder.deleteCharAt(builder.length()-1);
			}
			builder.delete(builder.length()-k.length(), builder.length());
		}
	}
	
	public static void printArray(HashMap<String, Integer> array){
		System.out.println("{");
		Set<String> index = array.keySet();
		Iterator<String> iterator = index.iterator();
		while(true){
			String s = iterator.next();
			System.out.print(s+":"+array.get(s));
			if(iterator.hasNext()){
				System.out.println(",");
			}else{
				break;
			}
		}
		System.out.println("\n}");
	}
	
	public static void printContainer(Container container){
		printContainer(container, "");
	}
	
	public static void printContainer(Container container, String tabs){
		System.out.println("\n"+tabs+"{");
		Set<String> keys = container.getKeys();
		Iterator<String> iterator = keys.iterator();
		
		while(true){
			String key = iterator.next();
			System.out.print(tabs+"'"+key+"':");
			Object o = container.get(key);
			if(o instanceof Integer){
				System.out.println(o);
			}else if(o instanceof ArrayList<?>){
				ArrayList<Integer> list =(ArrayList<Integer>)o; 
				System.out.print(tabs+"[");
				for(int i: list){
					System.out.print(i);
					if(!(list.indexOf(i)==list.size()-1)) System.out.print(", ");
				}
				System.out.print("]");
			}else{
				printContainer((Container)o, tabs+"\t");
			}
			if(iterator.hasNext()){
				System.out.println(",");
			}else{
				break;
			}
		}
		System.out.println(tabs+"}");
	}
	
}

