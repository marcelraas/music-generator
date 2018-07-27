import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import stft


def set_style():
    matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
    matplotlib.rcParams['lines.linewidth'] = 2
    matplotlib.rcParams['axes.linewidth'] = 1.5
    matplotlib.rcParams['font.size'] = 18
    matplotlib.rcParams['xtick.major.size'] = 5
    matplotlib.rcParams['xtick.major.width'] = 2
    matplotlib.rcParams['ytick.major.size'] = 5
    matplotlib.rcParams['ytick.major.width'] = 2
    matplotlib.rcParams['figure.figsize'] = (16.0, 8.0)


def stft_plot(data, rate, window_size=4096, vmin=0, vmax=0.5, max_freq=None):

    f_vec, t_vec, z = stft(data, rate, nperseg=window_size)
    plt.pcolormesh(t_vec, f_vec, np.abs(z), vmin=vmin, vmax=vmax)

    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')

    if max_freq is not None:
        plt.ylim(0, max_freq)
    
