import pytest

import numpy as np

from music_generator.analysis.play import play_array


@pytest.fixture(scope='module')
def sine_wave() -> np.ndarray:
    x = np.arange(0, 1, 1./44100)
    return np.sin(2*np.pi*x*100)


def test_player(sine_wave):
    pass
    # play_array(sine_wave)

