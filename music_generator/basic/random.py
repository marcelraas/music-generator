import numpy as np

from music_generator.musical.notes import Note
from music_generator.musical.scales import GenericScale

from music_generator.synthesizer.oscillators import SineOscillator
from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.musical.chords import MajorChordDefinition, MinorChordDefinition, ChordInScaleDefinition


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


# def monophonic_notes(n_notes,
#                      note_duration,
#                      amp,
#                      osc=SineOscillator(44100)):
#
#     octs = np.random.randint(3, 4, size=n_notes)
#     i_note = np.random.randint(0, notes, size=n_notes)
#     symbols = NOTES_DF.iloc[i_note].symbol
#
#     freqs = [Note(s, o).frequency()
#              for s, o in zip(symbols, octs)]
#
#     y = np.concatenate(list(map(lambda f: osc.generate(amp,
#                                                        note_duration,
#                                                        f,
#                                                        osc.phase),
#                                 freqs)))
#
#     return y


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


def monophonic_scale(n_notes,
                     note_duration,
                     amp,
                     scale: GenericScale,
                     osc=SquareOscillator(44100)):
    """Reimplementation of monophonic_random, using oscillator class"""

    notes = np.array(scale.generate(4, 5))
    freqs = np.array([n.frequency() for n in notes])

    p = [0.025, 0.1, 0.1, 0.1, 0.025, 0.1, 0.1, 0.1, 0.025]
    p = p / np.sum(p)

    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             n_notes - 1, p=p)

    rw = np.zeros(n_notes)
    rw[0] = np.random.randint(0, len(freqs))
    for i, step in enumerate(steps):
        rw[i+1] = rw[i] + step
        if rw[i+1] >= len(freqs):
            rw[i+1] = len(freqs) - 1 - (rw[i+1] - len(freqs))
        if rw[i+1] < 0:
            rw[i+1] = 0 - (rw[i+1] - 0)

    # ix = np.random.randint(0, len(freqs), size=n_notes)

    notes = notes[rw.astype(int)]
    # chord = MinorChordDefinition()
    cisd = ChordInScaleDefinition(scale)

    y = np.concatenate(list(map(
        lambda f: osc.generate_chord(cisd.generate_chord(f), note_duration, amp, osc.phase), notes)))

    return y
