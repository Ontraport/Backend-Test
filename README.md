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


----
# Notes on my solution
----

### Setup, testing, and test coverage

You will need **Python 3.6+**. I tested it on a GNU/Linux system. All of these commands are intended to be run from the project's root directory.

(Optional, but highly recommended) setting up and activating a virtual python environment:
```bash
$ python3.6 -m venv ontraport_venv
$ . ontraport_venv/bin/activate
```
To get out of the virtual environment afterwards:
```bash
$ deactivate
```

Installing requirements:
```bash
$ pip install -r requirements.txt
```

Static analysis (mypy):
```bash
$ mypy flatten/flatten.py
```

Running tests:
```bash
$ python -m pytest
```

Test coverage (currently 96% if you're curious):
```bash
$ python -m pytest --cov=flatten
```

----
### Use

The help screen:
```bash
$ flatten/flatten.py -h
Flatten: a tool for flattening (and expanding) multidimensional lists and dictionaries.

Usage:
  flatten.py (-e | -f) FILE
  flatten.py (-h | --help)
  flatten.py (-v | --version)

Options:
  -e --expand   Expand a file. Read from standard input if "-" is supplied as the file name.
  -f --flatten  Flatten a file. Read from standard input if "-" is supplied as the file name.
  -h --help     Show this screen.
  -v --version  Show version.
```

Flattening a file:
```bash
$ flatten/flatten.py --flatten tests/test_files/supplied_input_expanded.txt 
{'eight/nine/ten': 11,
 'one/four/0': 5,
 'one/four/1': 6,
 'one/four/2': 7,
 'one/two': 3}
```

Expanding a file:
```bash
$ flatten/flatten.py --expand tests/test_files/supplied_input_flattened.txt 
{'eight': {'nine': {'ten': 11}}, 'one': {'four': [5, 6, 7], 'two': 3}}
```

Reading from stdin works exactly as the help screen says. Try it out!
