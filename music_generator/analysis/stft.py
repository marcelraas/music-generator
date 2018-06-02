import numpy as np
from scipy.fftpack import rfft, irfft

from music_generator.basic.utils import parallel_apply_along_axis


def forward_stft(data, stft_sample_size=4096, stft_stride=256, window=None):
    stft_ix = np.arange(0, len(data) - stft_sample_size, stft_stride)
    stft_samples = []
    for ix in stft_ix:
        sample = data[ix:ix + stft_sample_size]
        stft_samples.append(sample)

    stft_samples = np.array(stft_samples)

    if window is not None:
        if len(window) != stft_sample_size:
            raise ValueError(f"Number of samples in window parameter should match the sample size ({stft_sample_size})")

        stft_samples *= np.outer(np.ones(stft_samples.shape[0]), window)

    transformed = parallel_apply_along_axis(rfft, 0, stft_samples)
    return transformed


def backward_stft(data, stft_stride, window=None):

    n_stft_samples = data.shape[0]
    stft_sample_size = data.shape[1]
    overlap_factor = stft_stride / stft_sample_size

    stft_samples = parallel_apply_along_axis(irfft, 0, data)

    stft_samples *= overlap_factor
    out = np.zeros(stft_stride * n_stft_samples + stft_sample_size)

    for ii, sample in enumerate(stft_samples):
        i_begin = ii*stft_stride
        i_end = i_begin + stft_sample_size
        out[i_begin:i_end] += sample

    return out
