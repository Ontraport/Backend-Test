/**
 * Convert single array to multidimensional container
 *
 * @param objList
 * @returns new object list
 */
function listToObjectConverter(objList) {
    const result = {}

    // loop over the object path
    for (const objectPath in objList) {
        // split the path into keys
        const keyList = objectPath.split('/')

        // create nested object and append the result
        let nestedObject = result
        let key

        // iterate until second last index
        while (keyList.length > 1) {
            // poll the keys from the list
            key = keyList.shift()

            // check if the last key is index
            if (!isNaN(keyList[0])) {

                // check if the key is present or not
                if (!nestedObject.hasOwnProperty(key)) {
                    // create list
                    nestedObject[key] = []
                }

                // push the value to the list
                nestedObject[key].push(objList[objectPath])
            } else {
                // check whether the key of the previous object is present or not
                // create new object
                nestedObject[key] = nestedObject[key] || {}
            }

            // update the nested object with the new object
            nestedObject = nestedObject[key]
        }

        // check whether the last key is not an index.
        if (isNaN(keyList[0])) {
            // set another key with the appropriate value
            nestedObject[keyList[0]] = objList[objectPath]
        }
    }

    return result
}

module.exports = listToObjectConverter;
