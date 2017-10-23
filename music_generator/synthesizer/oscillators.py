import numpy as np


class Generator(object):
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.phase = 0

    @property
    def phase_step(self):
        return 1. / self.sample_rate

    def duration_in_samples(self, duration):
        return duration * self.sample_rate


class SineOscillator(Generator):
    def __init__(self, sample_rate):
        Generator.__init__(self, sample_rate)
        pass

    def generate(self, amplitude, duration, frequency, phase):

        time_vec = np.arange(0, duration, self.phase_step)
        phase_vec = time_vec * 2 * np.pi * frequency + phase

        self.phase = phase_vec[-1]

        return np.sin(phase_vec) * amplitude

