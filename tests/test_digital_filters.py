import pytest
import numpy as np

from music_generator.basic.random import generate_dataset
from music_generator.musical.timing import Tempo
from music_generator.musical.scales import GenericScale
from music_generator.basic.signalproc import SamplingInfo

from music_generator.effects import digital_filters
from music_generator.analysis.play import play_array
from music_generator.basic import signalproc


@pytest.fixture
def lead():
    lead = generate_dataset(n_measures=4,
                            tempo=Tempo(120),
                            scale=GenericScale('C', [0, 2, 3, 5, 7, 8, 10]),
                            sampling_info=SamplingInfo(44100))[1][2]

    lead = np.concatenate((lead, np.zeros(shape=44100)), axis=0)
    return lead



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


def test_iir_filter(lead):


    iir = digital_filters.IirFilter([-0.8], [8000], [0.8], [8000])
    fx = iir.apply(lead)
    wet = signalproc.mix_at(lead, -fx, 0)
    play_array(fx, norm=1)

    pass


def test_allpass_comb_reverb(lead):

    allpass = digital_filters.CombAllPassReverb(np.linspace(0.9, 0.95, 10), np.linspace(500, 3000, 10))
    fx = allpass.apply(lead)
    wet = signalproc.mix_at(lead, fx, 0)
    play_array(fx, norm=1)
    pass
