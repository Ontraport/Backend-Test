const input = {
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

const expected = {
  'one/two': 3,
  'one/four/0': 5,
  'one/four/1': 6,
  'one/four/2': 7,
  'eight/nine/ten': 11,
};

const DELIMITER = '/';

function makeTag(tag, key) {
  return tag ? `${tag}${DELIMITER}${key}` : key;
}

function processArray(tag, array) {
  let count = 0;
  return array.map((e) => {
    const newPrefix = makeTag(tag, count);
    count += 1;
    return processElement(newPrefix, e); // eslint-disable-line no-use-before-define
  });
}

function processObject(tag, obj) {
  const properties = Object.entries(obj);
  return properties.map(([key, value]) => {
    const newPrefix = makeTag(tag, key);
    return processElement(newPrefix, value); // eslint-disable-line no-use-before-define
  });
}

function processElement(tag, value) {
  if (Array.isArray(value)) {
    return processArray(tag, value);
  }
  if (typeof value === 'object') {
    return processObject(tag, value);
  }
  return { [tag]: value };
}

function flatten(param) {
  const result = processElement('', param).flat(Infinity);
  return Object.assign(...result);
}

function expand(source) {
  const result = {};
  const props = Object.entries(source);

  props.forEach(([key, value]) => {
    const paths = key.split(DELIMITER);
    const pathsCount = paths.length;
    let elements = result;

    for (let level = 0; level < pathsCount; level += 1) {
      const path = paths[level];
      if (!elements[path]) {
        elements[path] = {};
      }

      // if next element is a number it is an array
      const elemNumber = Number(paths[level + 1]);
      if (!Number.isNaN(elemNumber)) {
        if (!Array.isArray(elements[path])) {
          elements[path] = [];
        }
        elements[path].push(Number(value));
        break;
      } else if (level === pathsCount - 1) {
        elements[path] = value; // at end
        break;
      } else {
        elements = elements[path];
      }
    }
  });
  return result;
}

/* eslint-disable no-console */

// tests
const flattened = flatten(input);
console.log('flatten success', JSON.stringify(flattened) === JSON.stringify(expected));

const expanded = expand(expected);
console.log('expand success', JSON.stringify(expanded) === JSON.stringify(input));
