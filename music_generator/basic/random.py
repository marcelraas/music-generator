import numpy as np

from music_generator.musical.timing import Signature, Tempo

from music_generator.basic.signalproc import SamplingInfo, apply_filter, mix_at
from music_generator.musical.notes import Note
from music_generator.musical.scales import GenericScale
from music_generator.synthesizer.instrument import Instrument

from music_generator.synthesizer.oscillators import SineOscillator
from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import AliasingSquareOscillator
from music_generator.synthesizer.oscillators import FilteredOscillator
from music_generator.synthesizer.oscillators import LinearAdsrGenerator
from music_generator.musical.chords import MajorChordDefinition, MinorChordDefinition, ChordInScaleDefinition
from music_generator.basic.utils import bounded_random_walk_mirror, elastic_bounded_random_walk

from music_generator.musical.score import Track, Measure


def make_lead_instrument(sampling_info):
    osc = AliasingSquareOscillator(sampling_info)
    lead_base_gen = LinearAdsrGenerator(1e-3, 100e-3, 0.3, 0.01, osc)
    lead_generator = FilteredOscillator(sampling_info,
                                        3000,
                                        filter_type="lowpass",
                                        base_generator=lead_base_gen,
                                        order=11)
    lead_instrument = Instrument(lead_generator)
    return lead_instrument


def make_accomp_instrument(sampling_info):
    osc = AliasingSquareOscillator(sampling_info)
    chord_base_gen = LinearAdsrGenerator(200e-3, 0.1e-6, 1.0, 500e-3, osc)
    chord_generator = FilteredOscillator(sampling_info, 1000, "lowpass", chord_base_gen, order=2)
    chord_instrument = Instrument(chord_generator)
    chord_instrument.velocity = 0.1
    return chord_instrument


def generate_chord_track(scale, tempo, signature, n_measures):
    cisd = ChordInScaleDefinition(scale)
    root_chord_scale = scale.generate(3, 4)

    chords = [cisd.generate_chord(root_chord_scale[0]),
              cisd.generate_chord(root_chord_scale[4]),
              cisd.generate_chord(root_chord_scale[5]),
              cisd.generate_chord(root_chord_scale[3])]

    chord_track = Track([])
    i = 0
    while i < n_measures:
        i_chord = i % 4

        measure = Measure(tempo, signature)
        for note in chords[i_chord].notes:
            measure.add_note(note, 0, 4)

        chord_track.measures.append(measure)
        i += 1

    return chord_track


def generate_lead_track(scale, tempo, signature, n_measures, n_notes_per_measure):
    n_notes = n_measures * n_notes_per_measure * 4
    p = [0.0005, 0.01, 0.1, 0.3, 0.0, 0.3, 0.1, 0.01, 0.0005]
    p = p / np.sum(p)
    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             n_notes - 1, p=p)
    notes = np.array(scale.generate(5, 6))
    rw = elastic_bounded_random_walk(steps, np.random.randint(0, len(notes)), 0, len(notes))
    notes = notes[rw.astype(int)]

    # TODO: use proper measures for, instead of one big measure with all notes
    measure = Measure(tempo, signature)
    for index, note in enumerate(notes):
        measure.add_note(note, index * 1 / 4., 1 / 4.)
    track = Track([measure])

    return track



def monophonic_scale(n_notes,
                     note_duration,
                     amp,
                     scale: GenericScale,
                     sampling_info):
    """Reimplementation of monophonic_random, using oscillator class"""

    n_measures = 17
    tempo = Tempo(90)
    signature = Signature(4, 4)
    n_notes_per_measure = 4

    lead_instrument = make_lead_instrument(sampling_info)
    chord_instrument = make_accomp_instrument(sampling_info)

    chord_track = generate_chord_track(scale, tempo, signature, n_measures)
    y = chord_instrument.generate_track(chord_track)

    lead_track = generate_lead_track(scale, tempo, signature, n_measures, n_notes_per_measure)
    y_lead = lead_instrument.generate_track(lead_track)

    y = mix_at(y, y_lead, at=0)

    return y


