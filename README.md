# ONTRAPORT Backend Skills Test

Hi, Thanks for checking us out

If you're interested in applying for the **Backend Engineer** team a great first step is to complete a brief test to allow us to assess your skills. You will find our Backend Engineer test below. Any language is fine, please note there are **two** questions:

1) Write a function that accepts a multi-dimensional container of any size and converts it into a one dimensional associative array whose keys are strings representing their value's path in the original container.

E.G.

```
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

turns into:

```
{
    'one/two':3,
    'one/four/0':5,
    'one/four/1':6,
    'one/four/2':7,
    'eight/nine/ten':11
}
```

2) Now write a separate function to do the reverse.

We want you to fork and then create a pull-reqest against this repository and we'll review it.

Thanks and good luck!

Ontraport Careers Team
