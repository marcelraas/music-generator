import numpy as np

from music_generator.basic.signalproc import SamplingInfo
from music_generator.musical.notes import Note
from music_generator.musical.scales import GenericScale

from music_generator.synthesizer.oscillators import SineOscillator
from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.musical.chords import MajorChordDefinition, MinorChordDefinition, ChordInScaleDefinition
from music_generator.basic.utils import bounded_random_walk_mirror


def monophonic_scale(n_notes,
                     note_duration,
                     amp,
                     scale: GenericScale,
                     osc=SquareOscillator(SamplingInfo(44100))):
    """Reimplementation of monophonic_random, using oscillator class"""

    notes = np.array(scale.generate(4, 5))

    p = [0.4, 0.1, 0.2, 0.1, 0.0, 0.1, 0.2, 0.1, 0.4]
    p = p / np.sum(p)

    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             int(n_notes/16) - 1, p=p)

    rw = bounded_random_walk_mirror(steps, np.random.randint(0, len(notes)), 0, len(notes))

    notes = notes[rw.astype(int)]
    cisd = ChordInScaleDefinition(scale)

    y = np.concatenate(list(map(
        lambda f: osc.generate_chord(cisd.generate_chord(f), note_duration * 16, amp, osc.phase), notes)))

    p = [0.0005, 0.01, 0.1, 0.5, 0.0, 0.5, 0.1, 0.01, 0.0005]
    p = p / np.sum(p)
    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             n_notes - 1, p=p)
    notes = np.array(scale.generate(6, 7))
    rw = bounded_random_walk_mirror(steps, np.random.randint(0, len(notes)), 0, len(notes))
    notes = notes[rw.astype(int)]

    y += np.concatenate(list(map(
        lambda f: osc.generate_note(f, note_duration, amp, osc.phase), notes)))

    return y
