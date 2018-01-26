import numpy as np

from music_generator.basic.signalproc import SamplingInfo, apply_filter
from music_generator.musical.notes import Note
from music_generator.musical.scales import GenericScale

from music_generator.synthesizer.oscillators import SineOscillator
from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.synthesizer.oscillators import FilteredOscillator
from music_generator.musical.chords import MajorChordDefinition, MinorChordDefinition, ChordInScaleDefinition
from music_generator.basic.utils import bounded_random_walk_mirror


def monophonic_scale(n_notes,
                     note_duration,
                     amp,
                     scale: GenericScale,
                     base_osc=SquareOscillator,
                     sampling_info=SamplingInfo(44100)):
    """Reimplementation of monophonic_random, using oscillator class"""

    base_osc = SquareOscillator(sampling_info)
    notes = np.array(scale.generate(4, 5))

    p = [0.1, 0.1, 0.3, 0.2, 0.0, 0.2, 0.3, 0.1, 0.1]
    p = p / np.sum(p)

    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             int(n_notes/16) - 1, p=p)

    rw = bounded_random_walk_mirror(steps, np.random.randint(0, len(notes)), 0, len(notes))

    notes = notes[rw.astype(int)]
    cisd = ChordInScaleDefinition(scale)

    chord_generator = FilteredOscillator(sampling_info, 2000, "lowpass", base_osc)
    # chord_generator = SquareOscillator(sampling_info)

    y = np.concatenate(list(map(
        lambda f: chord_generator.generate_chord(cisd.generate_chord(f), note_duration * 16, amp, 0), notes)))

    # y = apply_filter(y, sampling_info, 2000)

    p = [0.0005, 0.01, 0.1, 0.3, 0.0, 0.3, 0.1, 0.01, 0.0005]
    p = p / np.sum(p)
    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             n_notes - 1, p=p)
    notes = np.array(scale.generate(6, 7))
    rw = bounded_random_walk_mirror(steps, np.random.randint(0, len(notes)), 0, len(notes))
    notes = notes[rw.astype(int)]

    lead_generator = FilteredOscillator(sampling_info, 10000, "lowpass", base_osc, order=1)
    # lead_generator = SquareOscillator(sampling_info)

    y_lead = np.concatenate(list(map(
        lambda f: lead_generator.generate_note(f, note_duration, amp, 0), notes)))

    # y_lead = apply_filter(y_lead, sampling_info, cutoff_freq=10000, order=1, type='lowpass')

    y += y_lead

    return y
