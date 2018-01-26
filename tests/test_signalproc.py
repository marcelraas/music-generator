from music_generator.basic.signalproc import SamplingInfo, apply_filter
from music_generator.synthesizer.oscillators import SineOscillator

import pytest
import matplotlib.pyplot as plt
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

