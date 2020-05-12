package com.xocevad.engineering.skills;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Vector;

/**
 * Implements functions specified by ONTRAPORT's online GitHub Backend-Test,
 * here named convertMultiToOne() and convertOneToMulti().
 */
public class Skills {
    
    /**
     * Converts a multi-dimensional hierarchal container to a one-dimensional
     * associative array, whose string keys represent paths in the hierarchy, and
     * containing the same ultimate values. Note array indexes, as well as map keys,
     * are converted to string path elements.
     * 
     * @param multiDim multi-dimensional container. It is an error to pass an Object
     *                 that is neither a Map nor an array.
     * 
     * @return one-dimensional associative array (Map).
     */
    public static Map<String, Object> convertMultiToOne(Object multiDim) {
        var result = new LinkedHashMap<String, Object>();
        if (multiDim instanceof Map) {
            addMapToByPathMap((Map<?,?>)multiDim, "", result);
        
        } else if (multiDim.getClass().isArray()) {
            addArrayToByPathMap((Object[])multiDim, "", result);
        
        } else {
            throw new IllegalArgumentException(String.format(
                    "unexpected type of argument multiDim: %s", multiDim.getClass()));
        }
        return result;
    }
    
    private static void addObjectToByPathMap(Object obj, String path, Map<String, Object> out) {
        // classify value: container or simple value
        if (obj == null) {
            addSingleToByPathMap(obj, path, out);
            
        } else if (obj instanceof Map) {
            addMapToByPathMap((Map<?,?>)obj, path, out);
        
        } else if (obj.getClass().isArray()) {
            addArrayToByPathMap((Object[])obj, path, out);
        
        } else {
            addSingleToByPathMap(obj, path, out);
        }
    }
    
    private static void addMapToByPathMap(Map<?,?> map, String path, Map<String, Object> out) {
        map.forEach((name, value) -> addNamedValueToByPathMap(name.toString(), value, path, out));
    }
    
    private static void addArrayToByPathMap(Object[] array, String path, Map<String, Object> out) {
        var nElements = array.length;
        for (int n = 0; n < nElements; ++n) {
            String name = Integer.toString(n);
            addNamedValueToByPathMap(name, array[n], path, out);
        }
    }
    
    private static void addSingleToByPathMap(Object obj, String path, Map<String, Object> out) {
        // not a container; a leaf value; record the path and value.
        out.put(path, obj);
    }
    
    private static void addNamedValueToByPathMap(
            String name,
            Object value,
            String path,
            Map<String, Object> out) {
        // append name to path
        if (path.length() > 0) {
            // not empty; needs path delimiter
            path += kPathDelimiter + name;
        } else {
            path += name;
        }
        addObjectToByPathMap(value, path, out);
    }

    //--------------------------------------------------------------------------------------------//

    /**
     * Converts a one-dimensional associative array, whose keys are strings
     * representing paths in a hierarchy, to a multi-dimensional hierarchal
     * container, containing the same ultimate values. Path elements are converted
     * to indexes into containers: either string keys into a Map, or integer indexes
     * into an array when appropriate.
     * 
     * @param byPath one-dimensional associative array (Map) whose keys represent
     *               paths.
     * 
     * @return multi-dimensional hierarchal container.
     */
    public static Object convertOneToMulti(Map<String, Object> byPath) {
        var root = new ContainerNode();
        byPath.forEach((path, value) -> {
            // they say split() doesn't treat arg as a (slow) regex if it's one char.
            var pathElements = path.split(kPathDelimiter, -1);
            var pathElemsList = Arrays.asList(pathElements); // backed by the array
            
            addValueToNodeAtPath(value, root, pathElemsList);
        });
        // Render Nodes to maps, arrays and objects.
        return root.render();
    }
    
    private static void addValueToNodeAtPath(
            Object value, ContainerNode node, List<String>pathElemsList) {

        //System.out.format("addValueToNodeAtPath(), path: %s", pathElemsList).println();
        
        var nPathElems = pathElemsList.size();
        var name = pathElemsList.get(0);
        if (nPathElems < 1) {
            throw new IllegalArgumentException("malformed path in map");
        } else if (nPathElems == 1) {
            // We've consumed all the path; time to insert the leaf value.
            //System.out.format("    inserting value: %s", value).println();
            node.put(name, new ObjectNode(value));
        } else {
            // We have multiple path elements; the object corresponding to the 
            // front element must be a container (or the paths were inconsistent
            // in which case throw).
            ContainerNode subNode;
            try {
                subNode = (ContainerNode)node.get(name);
            } catch (ClassCastException x) {
                throw new IllegalArgumentException("inconsistent paths in map", x);
            }
            if (subNode == null) {
                // First time encountering this name within this node, so create the subNode.
                subNode = new ContainerNode();
                node.put(name, subNode);
            }
            // subList will be backed by same array
            addValueToNodeAtPath(value, subNode, pathElemsList.subList(1, nPathElems));
        }
    }
    
    // Node in a tree, representing either a single value, or a container.  We don't know, while
    // parsing path-value pairs, if a container should be an array, so all containers are Maps.
    // Once all containers are populated and all keys are observed, we can determine that a
    // particular container should have been an array.  The render() abstraction allows such
    // ContainerNode to substitute an array for the map.  Thus recursive render() is necessary
    // to replace a tree of Nodes with a tree of Map, Object[] and Object values.
    private interface Node {
        Object render();
    }
    
    // Node for a single-object value
    private static class ObjectNode implements Node {

        ObjectNode(Object obj) {
            this.object = obj;
        }
        
        @Override
        public Object render() {
            return object;
        }
        
        private Object object;
    }
    
    // Node for a container (map or array)
    private static class ContainerNode implements Node {
        
        public void put(String name, Object value) {
            map.put(name, value);
            if (integerIndexes && !nameLooksLikeIntegerIndex(name)) {
                integerIndexes = false;
            }
        }
        
        public Object get(String name) {
            return map.get(name);
        }
        
        @Override
        public Object render() {
            // Replace all the contained Nodes with their wrapped Objects:
            // render all the entries recursively.
            for (var key : map.keySet()) {
                var value = (Node)map.get(key);
                map.put(key, value.render());
            }
            if (integerIndexes) {
                // all keys look like integers; convert the Map to an array.
                return intStrIndexedMapToArray(map);
            }
            return map;
        }
        
        private boolean nameLooksLikeIntegerIndex(String name) {
            try {
                var n = Integer.parseInt(name);
                // array indexes must be non-negative
                return (n >= 0);
            } catch (NumberFormatException x) {
                return false;
            }
        }
        
        private Object[] intStrIndexedMapToArray(Map<String, Object> map) {
            // The map might represent a sparse array, with index value(s) greater than the
            // size of the map.  Use a Vector that can grow to the size needed, rather than
            // a fixed-length array matching the map size.
            var vector = new Vector<Object>(map.size());
            vector.setSize(map.size());
            map.forEach((name, value) -> {
                int n = Integer.parseInt(name);
                if (n >= vector.size()) {
                    vector.setSize(n + 1);
                }
                vector.set(n, value);
            });
            return vector.toArray();
        }

        private Map<String, Object> map = new LinkedHashMap<>();
        
        private boolean integerIndexes = true;
        
    }

    //--------------------------------------------------------------------------------------------//

    private static final String kPathDelimiter = "/";
    
}
