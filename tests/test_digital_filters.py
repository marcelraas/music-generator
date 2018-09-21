import pytest
import numpy as np

from music_generator.basic.random import generate_dataset
from music_generator.musical.timing import Tempo
from music_generator.musical.scales import GenericScale
from music_generator.basic.signalproc import SamplingInfo

from music_generator.effects import digital_filters
from music_generator.analysis.play import play_array


@pytest.fixture
def lead():
    return generate_dataset(n_measures=8,
                            tempo=Tempo(120),
                            scale=GenericScale('C', [0, 2, 3, 5, 7, 8, 10]),
                            sampling_info=SamplingInfo(44100))[1][2]


def test_fir_filter(lead):

    df = digital_filters.FirFilter([0.2], [4096*2])

    dry = lead
    fx = df.apply(lead)

    # wet = fx - dry
    play_array(fx)

    pass


def test_reverb_filter(lead):

    df = digital_filters.FirFilter(np.linspace(0.1, 0.0, 256), np.arange(256) * 512)

    dry = lead
    fx = df.apply(lead)

    # wet = fx - dry
    play_array(fx)
