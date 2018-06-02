import pytest

import numpy as np
import matplotlib.pyplot as plt

import music_generator.analysis.stft as stft
from music_generator.basic.utils import match_dims_by_clipping_tail


@pytest.fixture(scope='function')
def input_signal():
    x = np.arange(0, 4 * 44100, 1)
    return np.sin(x * 440 * 2 * np.pi / 44100)


def test_forward_stft_dimensionality(input_signal):
    window = np.ones(4096)
    transformed = stft.forward_stft(input_signal, 4096, 256, window)

    assert transformed.shape[1] == 4096


def test_forward_and_backward_stft_yields_original_input(input_signal):

    ssz = 4096
    transformed = stft.forward_stft(input_signal, ssz, 256)

    back = stft.backward_stft(transformed, stft_stride=256)

    orig, back = match_dims_by_clipping_tail(input_signal, back)
    n = len(input_signal)

    assert np.all(np.isclose((orig - back)[ssz:n-ssz], 0, atol=1E-9))

