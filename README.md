# Music-generator

A python library for generating random music

## Setup

Create virtual env:

```$ python3 -m virtualenv venv```

Activate it:

```$ source venv/bin/activate``` 

Install packages:

```$ pip install -r requirements.txt```

## Running

**Before running anything**, append the `PYTHONPATH` variable to the project root dir:

```bash
$ export PYTHONPATH=</path/to/music-generator>:${PYTHONPATH}
```

Run tests (this will make sound, so you might want to mute your speakers):

```
$ py.test tests
```

Generate music:

```
$ python scripts/gen_random.py
```






