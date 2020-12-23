const objectToListConverter = require("./converters/objectToListConverter");
const listToObjectConverter = require("./converters/listToObjectConverter");

// predefined json object
let jsonObj = {
    one: {
        two: 3,
        four: [5, 6, 7],
    },
    eight: {
        nine: {
            ten: 11,
        },
    },
};

/**
 * This function converts multidimensional container to single array
 * and again converts the single array to multidimensional container.
 *
 * @param jsonObj
 * @returns {*|{}}
 */
function main(jsonObj) {
    let list = objectToListConverter(jsonObj)
    let newJsonObj = listToObjectConverter(list)

    console.log(list)
    console.log(newJsonObj)

    return newJsonObj
}

main(jsonObj)

module.exports = main;
