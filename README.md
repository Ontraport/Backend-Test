my solution to Ontraport's backend skills test. two implementations: one in javascript, and one in ruby

# Original Question

>1) Write a function that accepts a multi-dimensional container of any size and converts it into a one dimensional associative array whose keys are strings representing their value's path in the original container.

>E.G.

>```
{
    'one':
    {
        'two': 3,
        'four': [ 5,6,7]
    },
    'eight':
    {
        'nine':
        {
            'ten':11
        }
    }
}
```

>turns into:

>```
{
    'one/two':3,
    'one/four/0':5,
    'one/four/1':6,
    'one/four/2':7,
    'eight/nine/ten':11
}
```

>2) Now write a separate function to do the reverse.
