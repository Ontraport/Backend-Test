//Question 1 Answer
/**
 * Convert Array to String
 * @param JSON Array
 * @returns Array as string
 */
function stringifyArray(jsonArr) {
    const solArr = [];
    for (let i = 0; i < jsonArr.length; i++) {
        let res = i.toString() + "/";
        if (typeof jsonArr[i] === "object") {
            solArr.push(res += stringifyObject(jsonArr[i]));
        } else if (Array.isArray(jsonArr[i])) {
            const s = stringifyArray(jsonArr[i]);
            for (const k in s) {
                solArr.push(res + k);
            }
        } else {
            solArr.push(i.toString() + ":" + jsonArr[i].toString());
        }
    }
    return solArr;
}

/**
 * Convert JSON Object to String
 * @param JSON Object
 * @returns Json Object as String
 */
function stringifyObject(jsonObj) {
    let res;
    const solArr = [];
    for (const key in jsonObj) {
        if (jsonObj.hasOwnProperty(key)) {
            if (typeof jsonObj[key] === "object") {
                res = stringifyObject(jsonObj[key]);
                for (const resKey in res) {
                    solArr.push(key.toString() + "/" + res[resKey]);
                }
            } else if (Array.isArray(jsonObj[key])) {
                res = stringifyArray(jsonObj[key]);
                for (const resKey in res) {
                    solArr.push(key.toString() + "/" + res[resKey]);
                }
            } else {
                solArr.push(key.toString() + ":" + jsonObj[key]);
            }
        }
    }
    return solArr;
}

/**
 *https://stackoverflow.com/questions/175739/built-in-way-in-javascript-to-check-if-a-string-is-a-valid-number
 * Check if string is a valid number
 * @param str string to check
 * @returns true if string is number, false otherwise
 */
function isNumeric(str) {
    if (typeof str != "string") return false // we only process strings!
    return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
        !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}

/**
 * Convert String array to Object
 * @param i index in string
 * @param text the string broken up in array
 * @param object the object to parse to
 * @returns the object parsed from string
 */
function toObject(i, text, object) {
    if (text[i].includes(":")) {
        const arr = text[i].split(":");
        text.splice(i, 1);
        text.push(...arr);
        if (isNumeric(text[i])) {
            /*
                        if (object.hasOwnProperty(text[i - 1])) {
                            object[text[i - 1]].push(text[i + 1]);
                            return object;
                        } else {
                            object[text[i - 1]] = [text[i + 1]];
                            return object;
                        }
            */
            return [parseInt(text[i + 1])];
        } else {
            object[text[i]] = parseInt(text[i + 1]);
            return object;
        }
    } else {
        if (isNumeric(text[i])) {
            const o = toObject(i + 1, text, {});
            /*
                        if (object.hasOwnProperty(text[i - 1])) {
                            object[text[i - 1]].push(o);
                            return object;
                        } else {
                            object[text[i - 1]] = o;
                            return object;
                        }
            */
            return [o];
        } else {
            var rec = toObject(i + 1, text, {});
            if (Array.isArray(rec)) {
                if (object.hasOwnProperty(text[i])) {
                    object[text[i]].push(rec[0]);
                } else {
                    object[text[i]] = rec;
                }
            } else {
                object[text[i]] = rec
            }
            return object;
        }
    }
}

/**
 * Put the object in parent object recursively
 * @param o the parent object
 * @param s the object to insert
 */
function putter(o, s) {
    let k = Object.keys(s)[0]
    if (o.hasOwnProperty(k)) {
        if (Array.isArray(s[k])) {
            o[k].push(s[k][0]);
        } else
            putter(o[k], s[k]);
    } else {
        o[k] = s[k];
    }
}

const testCase = {
    'one':
        {
            'two': 3,
            'four': [5, 6, 7]
        },
    'eight':
        {
            'nine':
                {
                    'ten': 11
                }
        }
};

const stringifiedTestCase = stringifyObject(testCase);
console.log("Object to string:");
console.log(stringifiedTestCase);

var o = {};
for (const rKey in stringifiedTestCase) {
    const text = stringifiedTestCase[rKey].split("/");
    const s = toObject(0, text, {});
    if (Array.isArray(s)) {
        if (o.hasOwnProperty(text[0])) {
            o[text[0]].push(s[0]);
        } else {
            o[text[0]] = s;
        }
    } else {
        putter(o, s);
    }
}
console.log("Back to original object:");
console.log(o);