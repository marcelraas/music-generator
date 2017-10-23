import numpy as np

from music_generator.synthesizer.oscillators import SineOscillator


def monophonic_random(n_notes, note_duration, sample_rate=44100):
    """Generate monophonic random music

    Args:
        n_notes (int): number of notes to generate
        note_duration (float): duration of notes
        sample_rate (int): sample rate

    Returns:
        np.array
    """

    min_freq = 0
    max_freq = 1600
    amp = 0.8

    n_samples_per_note = sample_rate * note_duration

    freqs = np.random.uniform(min_freq, max_freq, size=n_notes)

    delta_phases = 1. / sample_rate * 2 * np.pi * freqs

    phase = np.cumsum(
        np.kron(delta_phases, np.ones(shape=(int(n_samples_per_note)))))

    y = amp * np.sin(phase)

    return y


def monophonic_random_osc(n_notes,
                          note_duration,
                          sample_rate=44100,
                          osc=SineOscillator):
    """Reimplementation of monophonic_random, using oscillator class"""

    min_freq = 0
    max_freq = 3200
    amp = 0.8

    sin = osc(sample_rate)

    freqs = np.random.uniform(min_freq, max_freq, size=n_notes)

    y = np.concatenate(list(map(lambda x: sin.generate(amp,
                                                       note_duration,
                                                       x,
                                                       sin.phase), freqs)))

    return y