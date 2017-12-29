import numpy as np


class SamplingInfo(object):
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    @property
    def phase_step(self):
        return 1. / self.sample_rate

    @property
    def nyquist(self):
        return self.sample_rate / 2

    def generate_silence(self, seconds):
        return np.zeros(shape=int(seconds * self.sample_rate))


def mix_at(array, y, at=0):
    assert len(y) + at <= len(array)
    at = int(at)
    array[at:(at+len(y))] += y

