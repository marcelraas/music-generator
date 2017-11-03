import numpy as np


class Generator(object):
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.phase = 0

    @property
    def phase_step(self):
        return 1. / self.sample_rate

    def get_phase_vector(self, duration, frequency, phase, update_phase=False):
        time_vec = np.arange(0, duration, self.phase_step)
        phase_vec = time_vec * 2 * np.pi * frequency + phase

        if update_phase:
            self.phase = phase_vec[-1]

        return phase_vec


    def duration_in_samples(self, duration):
        return duration * self.sample_rate


class SineOscillator(Generator):
    def __init__(self, sample_rate):
        Generator.__init__(self, sample_rate)

    def generate(self, amplitude, duration, frequency, phase):

        return np.sin(self.get_phase_vector(duration, frequency, phase, update_phase=True)) * amplitude


class AdditiveOscillator(Generator):
    def __init__(self, sample_rate, harmonics):
        Generator.__init__(self, sample_rate)
        self.harmonics = np.array(harmonics)

    def generate(self, amplitude, duration, frequency, phase):

        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        sins = np.sin(phase_vec)

        ix = np.arange(0, len(phase_vec))
        step_harm = (np.arange(0, len(self.harmonics)) + 1)

        max_harm = self.sample_rate / 2 / frequency

        harmonics = self.harmonics[step_harm < max_harm]
        step_harm = step_harm[step_harm < max_harm]

        ix_harm = np.tensordot(step_harm, ix, axes=0)
        ix_harm = ix_harm % len(phase_vec)

        generated = np.tensordot(amplitude * harmonics, sins[ix_harm], axes=1)

        return generated


class SquareOscillator(AdditiveOscillator):
    def __init__(self, sample_rate):
        k = np.arange(1, sample_rate/50)
        harmonics = 1 / k
        harmonics[np.arange(1, len(harmonics), 2)] = 0
        AdditiveOscillator.__init__(self, sample_rate, harmonics)


class AliasingSquareOscillator(Generator):
    def __init__(self, sample_rate):
        Generator.__init__(self, sample_rate)

    def generate(self, amplitude, duration, frequency, phase):

        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        return amplitude * np.sign(np.sin(phase_vec))




