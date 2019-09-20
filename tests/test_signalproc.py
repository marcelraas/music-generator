from music_generator.basic.signalproc import SamplingInfo, apply_filter
from music_generator.synthesizer.oscillators import SineOscillator
from music_generator.analysis.play import play_array

import pytest
import matplotlib.pyplot as plt
import music_generator.basic.signalproc as signalproc
import numpy as np


def test_apply_filter():
    """Testing low- and high-pass filters

    Note that the hard-coded test values are not exact and are merely checking
    if the function yield reasonable behaviour.
    """

    amp = 1
    sampling_info = SamplingInfo(44100)
    osc = SineOscillator(sampling_info)
    data = osc.generate(amplitude=amp, duration=1, frequency=440, phase=0)

    y = apply_filter(data, sampling_info, 440, 5, 'lowpass')
    assert np.max(y) <= 0.55 * amp
    assert np.max(y) >= 0.45 * amp

    y = apply_filter(data, sampling_info, 220, 5, 'lowpass')
    assert np.max(y) <= 0.05 * amp

    y = apply_filter(data, sampling_info, 220, 5, 'highpass')
    assert np.max(y) >= 0.95 * amp

    pass


def test_blit():
    sampling_info = SamplingInfo(44100)

    x = np.arange(0, 1., 1/44100.) * 440 * 2 * np.pi
    y = signalproc.blit(sampling_info, x, 440, 0, -1)

    plt.plot(x, y)
    # plt.show()

    pass


def test_bl_square():
    sampling_info = SamplingInfo(44100)

    x = np.arange(0, 1., 1/44100.) * 1440 * 2 * np.pi
    pos = signalproc.blit(sampling_info, x, 1440, 0, -1)
    neg = signalproc.blit(sampling_info, x, 1440, np.pi, -1)

    y = np.cumsum(pos - neg)
    # y = pos

    plt.plot(x, y)
    # plt.show()
    # play_array(y)

    pass



# def test_integrated_bipolar_blit():
#     pos = WaveTable.from_func(4096, np.sinc)
#     neg = WaveTable.from_func(4096, lambda x: -np.sinc(x + np.pi))
#
#     bl_square = WaveTable(np.cumsum(pos.get_samples() + neg.get_samples()))
#
#     phase_vec = np.arange(0, 8*np.pi, 8*np.pi/501)
#     plt.plot(phase_vec, bl_square.eval(phase_vec))
#     plt.show()
#
#     pass




