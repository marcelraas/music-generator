from scipy import signal, fftpack
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

    def get_period(self, frequency):
        return self.sample_rate / frequency

    def generate_silence(self, seconds):
        return np.zeros(shape=int(seconds * self.sample_rate))

    def __eq__(self, other):
        return self.sample_rate == other.sample_rate

    def __lt__(self, other):
        return self.sample_rate < other.sample_rate


# TODO: make this a reliable unit tested function that can handle all corner cases
def mix_at(array, y, at=0):
    if len(y) + at >= len(array):
        n_extra_samples = int(len(y) + at - len(array))
        array = np.concatenate(
            (array, np.zeros(shape=n_extra_samples)))
    at = int(at)
    array[at:(at+len(y))] += y

    return array


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


def digital_sinc(x, m):
    """Digital sinc function

    See https://www.music.mcgill.ca/~gary/307/week5/bandlimited.html for more details.

    Args:
        x (np.array[float]): input x-values to evaluate
        m (int): number of harmonics

    Returns:
        np.array[float]
    """
    denom = m * np.sin(np.pi * x / m)

    use_normal_term = np.abs(denom) > 1e-12
    normal_term = np.divide(np.sin(np.pi * x), denom, where=use_normal_term)
    hopital_term = np.divide(np.cos(np.pi*x), np.cos(np.pi*x/m), where=~use_normal_term)

    y = np.where(use_normal_term, normal_term, hopital_term)

    # # TODO: in case of numerical issue, limit is always 1, solve better way
    y[np.isnan(y)] = 1
    return y


def blit(sampling_info: SamplingInfo, phase_vec, frequency, phase_shift, num_harm=-1):
    """Generate a bandwidth limited impulse train (BLIT)

    Args:
        sampling_info (SamplingInfo): sampling information
        phase_vec (np.array[float]): phase vector in radians
        frequency (float): frequency
        phase_shift (float): phase shift in radians
        num_harm (int): number of harmonics
            when -1, the number of harmonics is such that the frequency of the highest harmonic is below the Nyquist
            frequency.

    Returns:
        np.array[float]
    """
    period = sampling_info.get_period(frequency)
    ph_shift_samples = int(phase_shift / 2 / np.pi * period)

    n = np.arange(0., len(phase_vec), 1.)
    n += ph_shift_samples

    # Determine number of harmonics based on Nyquist
    if num_harm == -1:
        num_harm = int(sampling_info.nyquist / frequency)
        num_harm = num_harm - (1 if (num_harm % 2 == 0) else 0)

    return num_harm / period * digital_sinc(n * num_harm / period, num_harm)


def bl_square(sampling_info: SamplingInfo, phase_vec, frequency, phase_shift, num_harm=-1):

    pos = blit(sampling_info, phase_vec, frequency, phase_shift, num_harm)
    neg = blit(sampling_info, phase_vec, frequency, phase_shift + np.pi, num_harm)

    return np.cumsum(pos - neg) * 4 - 2



