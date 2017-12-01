import numpy as np

from music_generator.musical.notes import NOTES_DF, Note

from music_generator.synthesizer.oscillators import SineOscillator
from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import SquareOscillator


def monophonic_random(n_notes, note_duration, sample_rate=44100):
    """Generate monophonic random music

    Args:
        n_notes (int): number of steps to generate
        note_duration (float): duration of steps
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


def monophonic_notes(n_notes,
                     note_duration,
                     amp,
                     osc=SineOscillator(44100)):

    octs = np.random.randint(3, 4, size=n_notes)
    i_note = np.random.randint(0, len(NOTES_DF), size=n_notes)
    symbols = NOTES_DF.iloc[i_note].symbol

    freqs = [Note(s, o).frequency()
             for s, o in zip(symbols, octs)]

    y = np.concatenate(list(map(lambda f: osc.generate(amp,
                                                       note_duration,
                                                       f,
                                                       osc.phase),
                                freqs)))

    return y


def monophonic_random_osc(n_notes,
                          note_duration,
                          amp,
                          osc=SquareOscillator(44100)):
    """Reimplementation of monophonic_random, using oscillator class"""

    min_freq = 0
    max_freq = 3600

    freqs = np.random.uniform(min_freq, max_freq, size=n_notes)

    y = np.concatenate(list(map(lambda f: osc.generate(amp,
                                                       note_duration,
                                                       f,
                                                       osc.phase),
                                freqs)))

    return y
