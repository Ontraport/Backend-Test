// helper functions for use in other functions
function isObject(value) {
  return (
    typeof value === "object" &&
    !Array.isArray(value) &&
    value !== null &&
    !(value instanceof Date)
  );
}

function isArray(value) {
  return Array.isArray(value);
}

/**
 * @description - returns the combined nested path by prepending key with path+/
 * @param {string | number} key - key that path should be prepended with
 * @param {string | undefined} path - existing path to add key to
 */
function getPath(key, path) {
  return `${path ? path + "/" : ""}${key}`;
}

/**
 * @param {object} container - object to be converted to single dimension array
 * @returns {object} - single dimension object where keys represent terminal paths of original object
 */
function convertMultiToSingleDimension(container) {
  if (!isObject(container)) {
    throw new Error("Container must be a plain object");
  }

  const flattenContainer = (value, path) => {
    if (!isObject(value) && !isArray(value)) {
      container[path] = value instanceof Date ? value.toISOString() : value;
    } else if (isArray(value)) {
      value.forEach((item, i) => flattenContainer(item, getPath(i, path)));
    } else {
      Object.keys(value).forEach((key) => {
        const temp = value[key];
        delete value[key];
        flattenContainer(temp, getPath(key, path));
      });
    }
  };

  flattenContainer(container);
}

/**
 * @param {Object} container - single dimensional object with paths as keys
 * @returns {Object} multi dimensional object.
 */
function convertSingleToMultiDimension(container) {
  if (!isObject(container)) {
    throw new Error("Container must be a plain object");
  }

  Object.keys(container).forEach((path) => {
    const keys = path.split("/");

    if (keys.length > 1) {
      let temp = container;

      keys.forEach((key, i) => {
        if (i == keys.length - 1) {
          const value = container[path];
          if (Array.isArray(temp)) {
            temp.push(value);
          } else {
            temp[key] = value;
          }
        } else {
          const nextLevelIsArray = !isNaN(parseInt(keys[i + 1]));

          temp[key] = temp[key] || (nextLevelIsArray ? [] : {});
          temp = temp[key];
        }
      });
      delete container[path];
    }
  });
}
