import pytest

import numpy as np
from music_generator.analysis.preprocessing import create_batches

import music_generator.analysis.preprocessing as pp


def test_read_wavefile():
    pass


def test_create_batches():

    x = np.arange(0, 1000, 1)

    batches = create_batches(x, 16, 5)

    assert len(batches) == 197  # (1000 - 16) / 5 + 1
    assert len(batches[0]) == 16

