from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import LinearAdsrGenerator
from music_generator.synthesizer.oscillators import AliasingSquareOscillator
from music_generator.basic.signalproc import SamplingInfo

import music_generator.synthesizer.oscillators as oscillators

from music_generator.analysis.play import play_array

import matplotlib.pyplot as plt
import numpy as np

import pytest

@pytest.fixture(scope="module")
def sampling_info():
    return SamplingInfo(44100)


def test_additive_osc():

    additive = AdditiveOscillator(SamplingInfo(44100), [1, 0.5, 0.25, 0.125])

    fx = additive.generate(0.5, 1, 440, 0)


def test_adsr_envelope(sampling_info):

    lag = LinearAdsrGenerator(10e-3, 10e-3, 0.9, 0.1, AliasingSquareOscillator(sampling_info))
    envelope = lag._generate_envelope(1)

    # Check the anchor-points of the envelope
    assert np.isclose(envelope[0], 0)
    assert np.isclose(envelope[int(10e-3 * 44100)], 1)
    assert np.isclose(envelope[int(20e-3 * 44100)], 0.9)
    assert np.isclose(envelope[int(1.0 * 44100)], 0.9)
    assert np.isclose(envelope[int(1.1 * 44100) - 1], 0, atol=0.01)


def test_adsr_generation(sampling_info):

    lag = LinearAdsrGenerator(100e-3, 100e-3, 0.8, 0.1, AliasingSquareOscillator(sampling_info))
    y = lag.generate(0.1, 1, 440)

    # Basic test, visual inspections can be uncommented below
    assert y is not None
    # play_array(y)
    # plt.plot(y)
    # plt.show()


