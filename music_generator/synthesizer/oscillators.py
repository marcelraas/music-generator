from scipy.interpolate import interp1d
import numpy as np
from copy import copy

from music_generator.signalproc.signalproc import SamplingInfo, apply_filter, bl_square


class Generator(object):
    def __init__(self, sampling_info: SamplingInfo):
        self.sampling_info = sampling_info
        self.phase = 0

    def get_phase_vector(self, duration, frequency, phase, update_phase=False):
        """Get a phase vector

        Args:
            duration (float): duration in seconds
            frequency (float): frequency in Hertz
            phase (float): phase in rad
            update_phase (bool): whether or not to update the internal phase

        Returns:
            phase_vector (np.array[float])
        """
        if phase is None:
            phase = self.phase

        time_vec = np.arange(0, duration, self.sampling_info.delta_t)
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


class AliasingSquareOscillator(Generator):
    def __init__(self, sampling_info: SamplingInfo):
        Generator.__init__(self, sampling_info)

    def generate(self, amplitude, duration, frequency, phase):

        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        return amplitude * np.sign(np.sin(phase_vec))


class WaveTable(object):

    def __init__(self, samples):
        self._x = np.arange(0, 2 * np.pi, 2 * np.pi / len(samples))
        self._y = copy(samples)
        self._interp_func = interp1d(self._x, self._y)

    def get_samples(self):
        return self._y

    @classmethod
    def from_func(cls, n_samples, func):
        x = np.arange(0, 2 * np.pi, 2 * np.pi / n_samples)
        y = func(x)
        return cls(y)

    def eval(self, phase_vec):
        phase_vec = phase_vec % 2*np.pi
        return self._interp_func(phase_vec)


class WaveTableOscillator(Generator):
    def __init__(self, sampling_info: SamplingInfo, wave_table: WaveTable):
        Generator.__init__(self, sampling_info)
        self.wave_table = wave_table

    def generate(self, amplitude, duration, frequency, phase):
        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        return amplitude * self.wave_table.eval(phase_vec)


class SquareOscillator(Generator):
    def __init__(self, sampling_info: SamplingInfo):
        Generator.__init__(self, sampling_info)

    def generate(self, amplitude, duration, frequency, phase):
        phase_vec = self.get_phase_vector(duration, frequency, phase, update_phase=True)
        return amplitude * bl_square(self.sampling_info, phase_vec, frequency, 0, -1)


class FilteredOscillator(Generator):
    def __init__(self,
                 sampling_info: SamplingInfo,
                 cutoff_freq: float,
                 filter_type: str,
                 base_generator: Generator,
                 order=5):
        Generator.__init__(self, sampling_info)
        self.cutoff_freq = cutoff_freq
        self.filter_type = filter_type
        self.base_generator = base_generator
        self.order = order
        self.couple_velocity = False

        assert self.base_generator.sampling_info == self.sampling_info, \
            "SamplingInfo of base_generator does not match the value in parameter sampling_info"

    def generate(self, amplitude, duration, frequency, phase=None):

        cutoff_freq = self.cutoff_freq if self.couple_velocity is False \
            else self.cutoff_freq * amplitude / self.couple_velocity

        y = self.base_generator.generate(amplitude, duration, frequency, phase)
        y = apply_filter(y, self.sampling_info, cutoff_freq, ftype=self.filter_type, order=self.order)
        return y


class LinearAdsrGenerator(Generator):
    def __init__(self, attack, decay, sustain, release, oscillator):
        Generator.__init__(self, oscillator.sampling_info)
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.oscillator = oscillator

        dt = self.sampling_info.delta_t

        self.attack_envelope = np.arange(0, attack, dt) / attack * 1 \
            if attack > 0 else np.array([])
        self.decay_envelope = np.arange(0, decay, dt) / decay * (sustain - 1) + 1 \
            if decay > 0 else np.array([])
        self.release_envelope = -np.arange(0, release, dt) / release * sustain + sustain \
            if release > 0 else np.array([])

        if self.release < 0:
            self.release = 0

    def _match_shapes(self, array, n_samples, max_mismatch=2):
        # TODO: this method is pretty ugly, can we solve it differently
        if abs(len(array) - n_samples) > max_mismatch:
            raise ValueError()
        if len(array) == n_samples:
            return array
        elif len(array) > n_samples:
            return array[0:n_samples]
        else:
            return np.concatenate((array[0:n_samples], np.zeros(shape=(n_samples - len(array),),)))

    def _generate_envelope(self, duration):

        # If note is shorter than attack + decay, append release after current phase and scale with current amp
        sustain_time = duration - self.attack - self.decay
        if sustain_time < 0:
            start = np.concatenate((self.attack_envelope, self.decay_envelope))
            samples_until_note_release = start[0:int(duration * self.sampling_info.sample_rate)]
            note_release_amp = samples_until_note_release[-1]
            factor = note_release_amp / self.sustain if self.sustain != 0 else 0
            return np.concatenate((samples_until_note_release, self.release_envelope * factor))

        sustain_samples = int(np.ceil((duration - self.attack - self.decay) / self.sampling_info.delta_t))
        sustain_envelope = np.array(sustain_samples*[self.sustain])

        return np.concatenate((self.attack_envelope, self.decay_envelope, sustain_envelope, self.release_envelope))

    def generate(self, amplitude, duration, frequency, phase=None):

        raw = self.oscillator.generate(amplitude,
                                       duration + self.release,
                                       frequency,
                                       phase)

        # TODO: due to rounding errors we have to pad 0's or remove a few samples from the envelope
        envelope = self._match_shapes(self._generate_envelope(duration), raw.shape[0])

        return raw * envelope





