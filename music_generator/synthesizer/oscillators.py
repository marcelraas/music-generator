from music_generator.basic.signalproc import SamplingInfo

import numpy as np


class Generator(object):
    def __init__(self, sampling_info: SamplingInfo):
        self.sampling_info = sampling_info
        self.phase = 0

    def get_phase_vector(self, duration, frequency, phase, update_phase=False):
        time_vec = np.arange(0, duration, self.sampling_info.phase_step)
        phase_vec = time_vec * 2 * np.pi * frequency + phase

        if update_phase:
            self.phase = phase_vec[-1]

        return phase_vec

    def generate_note(self, note, duration, amplitude, phase=None):
        if phase is None:
            phase = self.phase
        return self.generate(amplitude, duration, note.frequency(), phase)

    def generate_chord(self, chord, duration, amplitude, phase=None):
        if phase is None:
            phase = self.phase

        result = None
        for note in chord.notes:
            self.phase = phase
            y = self.generate(amplitude, duration, note.frequency(), self.phase)
            if result is not None:
                result += y
            else:
                result = y

        return result

    def duration_in_samples(self, duration):
        return duration * self.sampling_info

    def generate(self, amplitude, duration, frequency, phase):
        raise NotImplementedError('Pure virtual function called')


class SineOscillator(Generator):
    def __init__(self, sampling_info: SamplingInfo):
        Generator.__init__(self, sampling_info)

    def generate(self, amplitude, duration, frequency, phase):

        return np.sin(self.get_phase_vector(duration, frequency, phase, update_phase=True)) * amplitude


class AdditiveOscillator(Generator):
    def __init__(self, sampling_info: SamplingInfo, harmonics):
        Generator.__init__(self, sampling_info)
        self.harmonics = np.array(harmonics)

    def generate(self, amplitude, duration, frequency, phase):

        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        sins = np.sin(phase_vec)

        ix = np.arange(0, len(phase_vec))
        step_harm = (np.arange(0, len(self.harmonics)) + 1)

        max_harm = self.sampling_info.nyquist / frequency

        harmonics = self.harmonics[step_harm < max_harm]
        step_harm = step_harm[step_harm < max_harm]

        ix_harm = np.tensordot(step_harm, ix, axes=0)
        ix_harm = ix_harm % len(phase_vec)

        generated = np.tensordot(amplitude * harmonics, sins[ix_harm], axes=1)

        return generated


class SquareOscillator(AdditiveOscillator):
    def __init__(self, sampling_info: SamplingInfo):
        k = np.arange(1, sampling_info.sample_rate / 50)
        harmonics = 1 / k
        harmonics[np.arange(1, len(harmonics), 2)] = 0
        AdditiveOscillator.__init__(self, sampling_info, harmonics)


class AliasingSquareOscillator(Generator):
    def __init__(self, sampling_info: SamplingInfo):
        Generator.__init__(self, sampling_info)

    def generate(self, amplitude, duration, frequency, phase):

        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        return amplitude * np.sign(np.sin(phase_vec))




