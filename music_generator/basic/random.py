import numpy as np


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

    freqs = np.random.uniform(min_freq, max_freq, size=int(n_notes) + 1)

    delta_phases = 1. / sample_rate * 2 * np.pi * freqs

    np.kron(delta_phases, np.ones(shape=(int(n_samples_per_note))))

    phase = np.cumsum(
        np.kron(delta_phases, np.ones(shape=(int(n_samples_per_note)))))
    y = amp * np.sin(phase)

    return y
