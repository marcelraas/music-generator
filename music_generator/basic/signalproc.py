from scipy import signal
from functools import total_ordering

import numpy as np
import matplotlib.pyplot as plt


@total_ordering
class SamplingInfo(object):
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    @property
    def delta_t(self):
        return 1. / self.sample_rate

    @property
    def nyquist(self):
        return self.sample_rate / 2

    def generate_silence(self, seconds):
        return np.zeros(shape=int(seconds * self.sample_rate))

    def __eq__(self, other):
        return self.sample_rate == other.sample_rate

    def __lt__(self, other):
        return self.sample_rate < other.sample_rate


def mix_at(array, y, at=0):
    assert len(y) + at <= len(array)
    at = int(at)
    array[at:(at+len(y))] += y


def apply_filter(data: np.array, sampling_info: SamplingInfo, cutoff_freq: float, order=5, type='lowpass'):
    """Apply filter

    Applies a Butterworth filter to the data.

    Args:
        data (np.array): data to be filtered
        sampling_info (SamplingInfo): sampling info instance
        cutoff_freq (float): cut-off frequency in Hertz
        order (int): order of the Butterworth filter
        type (str): lowpass, highpass, bandpass or bandstop

    Returns:

    """
    normal_cutoff = cutoff_freq / sampling_info.nyquist
    # noinspection PyTupleAssignmentBalance
    b, a = signal.butter(order, normal_cutoff, btype=type, analog=False, output='ba')
    return signal.filtfilt(b, a, data, padlen=150)
