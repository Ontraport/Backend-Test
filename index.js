const testData = {
  one: {
    two: 3,
    four: [5, 6, 7]
  },
  eight: {
    nine: {
      ten: 11
    }
  }
};

/**
 * Returns the provided argument, only if it is an array.
 * Otherwise returns and empty array
 * @param {any[]} arr list
 */
function safeArray(arr) {
  if (Array.isArray(arr)) return arr;

  return [];
}

/**
 * Create an array from a given path
 * @param {*} currentObject the current "state"
 * @param {*} parts parts of the path
 */
function toArray(currentObject = [], parts) {
  const [index, value, ...left] = parts;
  const arr = safeArray(currentObject);

  arr[index] = left.length ? toObject(arr[index], [value, ...left]) : value;

  return arr;
}

/**
 * Create an object from a given path
 * @param {*} currentObject the current "state"
 * @param {*} parts parts of the path
 */
function toObject(currentObject = {}, parts) {
  const [key, ...left] = parts;
  const hasNextPath = left.length !== 1;

  if (!isNaN(key)) return toArray(currentObject, parts);

  const newObject = { ...currentObject };

  newObject[key] = hasNextPath ? toObject(currentObject[key], left) : left[0];

  return newObject;
}

/**
 * Create an one dimensional object describing all properties of the given item
 * @param {*} item the object
 * @param {*} basePath
 */
function describeObject(item, basePath = "") {
  if (typeof item == "object") {
    return Object.keys(item).reduce(
      (acc, key) => ({
        ...acc,
        ...describeObject(item[key], !basePath ? key : `${basePath}/${key}`)
      }),
      {}
    );
  }

  return { [basePath]: item };
}

/**
 * Create an n-dimensional object given the description object
 * @param {} objectDescription
 */
function objectFromDescription(objectDescription) {
  const pathParts = Object.keys(objectDescription).map(key => [
    ...key.split("/"),
    objectDescription[key]
  ]);

  return pathParts.reduce(
    (acc, path) => ({ ...acc, ...toObject(acc, path) }),
    {}
  );
}

const objectDescription = describeObject(testData);
const object = objectFromDescription(objectDescription);

console.log(objectDescription)
console.log(JSON.stringify(objectFromDescription(object), null, 2));
