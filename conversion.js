var sampleInput = {
  'one': {
    'two': 3,
    'four': [5, 6, 7]
  },
  'eight': {
    'nine': {
      'ten': 11
    }
  }
};

var sampleOutput = {
  'one/two': 3,
  'one/four/0': 5,
  'one/four/1': 6,
  'one/four/2': 7,
  'eight/nine/ten': 11
};

function getKeyValue(path, object) {
  return path.reduce((cb, v) => (cb && cb[v]) ? cb[v] : null, object);
}

function deepMerge(target, source) {
  for (let key of Object.keys(source)) {
    if (source[key] instanceof Object && key in target) {
      Object.assign(source[key], deepMerge(target[key], source[key]));
    }
  }

  Object.assign(target || {}, source);
  return target;
}

function flattenObject(obj, path, flatObj) {
  for (var key in obj) {
    if (obj.hasOwnProperty(key)) {
      // if branch
      if (typeof obj[key] === "object" && !Array.isArray(obj[key])) {
        flattenObject(obj[key], path !== '' ? path + '/' + key : path + key, flatObj);
      } else if (typeof obj[key] === "object" && Array.isArray(obj[key])) {
        // if leaf - array
        for (var i = 0; i < obj[key].length; ++i) {
          flatObj[path + '/' + key + '/' + i] = obj[key][i];
        }
      } else {
        // if leaf - elem
        flatObj[path + '/' + key] = obj[key];
      }
    }
  }

  return flatObj;
}

function unflattenObject(obj) {
  var finalObj = {};

  for (var key in obj) {
    if (obj.hasOwnProperty(key)) {
      var subObj = finalObj;
      var keys = key.split('/');

      for (var i = keys.length - 1; i >= 0; --i) {
        var endObj = (i === keys.length - 1 && !isNaN(keys[keys.length - 1])) ? [] : {};

        if (i === keys.length - 1 && isNaN(keys[i])) {
          // assign value
          endObj[keys[i]] = obj[key];
        } else if (isNaN(keys[i])) {
          // nest objects
          endObj[keys[i]] = subObj;
        } else {
          // concat or push first array elem
          var existingArray = getKeyValue(keys.slice(0, keys.length - 1), subObj);
          endObj = existingArray ? [...existingArray, obj[key]] : [obj[key]];
        }

        subObj = endObj;
      }

      finalObj = deepMerge(subObj, finalObj);
    }
  }

  return finalObj;
}

function verifyTransformedObject(obj, test) {
  return JSON.stringify(Object.keys(obj).sort()) === JSON.stringify(Object.keys(test).sort());
}

// console.dir(flattenObject(sampleInput, '', {}));
console.log("----- Flat Test:", verifyTransformedObject(flattenObject(sampleInput, '', {}), sampleOutput));

// console.dir(unflattenObject(sampleOutput));
console.log("----- Deep Test:", verifyTransformedObject(unflattenObject(sampleOutput), sampleInput));
