/**
 * Convert multidimensional container to single array
 *
 * @param jsonObj
 * @param objPath
 * @param objList
 * @returns {{}}
 */
function objectToListConverter(jsonObj, objPath = null, objList = {}) {

    // check whether the last object is number
    // if its number then its the index
    if (typeof jsonObj === 'number') {
        // append the object
        objList = {...objList, [objPath]: jsonObj}
    } else if (jsonObj == null) {
        // base condition
        return objList
    }

    // loop over json object
    for (const [key, value] of Object.entries(jsonObj)) {
        // initially objPath will be null so dont concatenate object path
        if (objPath === null) {
            // pass the key as object path
            objList = objectToListConverter(value, key, objList)
        } else {
            // append the object path with key
            // so that we can get complete path
            objList = objectToListConverter(value, `${objPath}/${key}`, objList)
        }
    }

    // return new objectList
    return objList
}

module.exports = objectToListConverter;
