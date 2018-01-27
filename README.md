# Music-generator

A python library for generating random music to be used as training set for instrument detection and score-generation from recorded audio with machine learning. 

> Truth is ever to be found in simplicity, and not in the multiplicity and confusion of things.
>
> Isaac Newton


I am making this music generator in addition to training data from a huge data set of recorded music for the following reasons:

- We can control the complexity of our problem (how many instruments, what type of instruments, type of rhythms, polyphone vs. monophone, etc.). 
- Since we are generating the data, the data set is infinite.


## Contents

The package offers:

* Basic music theory:
	* Notes and their frequencies (tuning of A4 other than 440 Hz is possible, only the scale-invariant, equal temperament is supported for now)
	* Scales: major/minor scales, a generic scale is also available
	* Chords: major/minor chords, augmented and diminished
	* Tempo, time signatures, measures
	* Tracks and scores
* Synthesizer module:
	* Basic oscillators: square, sine, additive sine (to be added: triangle, wavetable synthesizer)
	* ADSR (attack-decay-sustain-release) enveloping for any generator
	* Butterworth filters
* Random music generation module:
	* Generate random melody using random walk


## Setup

Create virtual env:

```$ python3 -m virtualenv venv```

Activate it:

```$ source venv/bin/activate``` 

Install packages:

```$ pip install -r requirements.txt```

## Running

**Before running anything**, append the project root dir to the the `PYTHONPATH` variable:

```bash
$ export PYTHONPATH=</path/to/music-generator>:${PYTHONPATH}
```

Run tests (this will make sound, so you might want to mute your speakers):

```
$ py.test tests
```

If you get matplotlib errors google for the solution (should be easy).

Generate music:

```
$ python scripts/gen_random.py
```






