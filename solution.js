#!/usr/bin/env node
"use strict";

// Note: This is ES6. In ES5, iterating over keys in an object requires taking
// more safeguards. I used this method because it extracts the indices of an
// array as if they were properties on a POJO, which is super convenient!
function flatten( container ) {
  var output = {};
  var flat;
  Object.keys( container ).forEach( (key) => {
    if( typeof container[key] === "object" ) {
      flat = flatten( container[key] );
      Object.keys( flat ).forEach( (subkey) => {
        output[key + "/" + subkey] = flat[subkey];
      });
    } else {
      output[key] = container[key];
    }
  });

  return output;
}

function deflatten( container ) {
  var keys = [];
  var output = {};
  var ref;
  Object.keys( container ).forEach( (key) => {
    keys = key.split("/");
    ref = output;
    keys.forEach( (subkey, index) => {
      // for every key except the last one, ensure object or array is nested.
      if( index < keys.length - 1 ) {
        if( !ref.hasOwnProperty( subkey ) ) {
          // here we're making a huge assumption: ints as subpaths will always mean an array index
          if( parseInt( keys[index + 1] ).toString() === keys[index + 1] ) {
            ref[ subkey ] = [];
          } else {
            ref[ subkey ] = {};
          }
        }
        ref = ref[ subkey ];
      // and for the last key, pass the value to this object (or array).
      } else {
        // index condition is because you can't reference individual values in an array
        ref[ subkey ] = container[ key ];
      }
    });
  });
  return output;
}

var unflattened = {
    'one':
    {
        'two': 3,
        'four': [5,6,7]
    },
    'eight':
    {
        'nine':
        {
            'ten':11
        }
    }
};

var flattened = {
    'one/two':3,
    'one/four/0':5,
    'one/four/1':6,
    'one/four/2':7,
    'eight/nine/ten':11
};

var test = {
  flatten: JSON.stringify( flatten( unflattened ) ) === JSON.stringify( flattened ),
  deflatten: JSON.stringify( deflatten( flattened ) ) === JSON.stringify( unflattened )
};

if( test.flatten && test.deflatten ) {
  console.log("'`,'`,'`,'`, YAY! Everything works. ,`',`',`',`'");
  //                       that's supposed to be confetti ^
} else {
  console.log("No party today :( These methods are broken:");
  Object.keys( test ).forEach( (key) => {
    if( !test[key] ) {
      console.log( " [FAIL] " + key);
    }
  });
}
