import numpy as np

from music_generator.signalproc.signalproc import SamplingInfo, mixdown
from music_generator.basic.utils import elastic_bounded_random_walk
from music_generator.music.chords import ChordInScaleDefinition
from music_generator.music.scales import GenericScale
from music_generator.music.score import Track, Measure
from music_generator.music.timing import Tempo, Signature
from music_generator.prefabs.basic_instruments import make_bass_instrument, make_lead_instrument, make_accomp_instrument


def generate_bass_track(scale, tempo, signature, n_measures):
    scale = scale.generate(1, 2)

    roots = [scale[0], scale[4], scale[5], scale[3]]

    track = Track([])
    i = 0
    while i < n_measures:
        i_note = i % 4

        note = roots[i_note]

        measure = Measure(tempo, signature)
        measure.add_note(note, 0, 0.5)
        measure.add_note(note, 1.0, 0.5)
        measure.add_note(note, 2.0, 0.125)
        measure.add_note(note, 2.5, 0.5)
        measure.add_note(note, 3.5, 0.25)

        track.measures.append(measure)
        i += 1

    return track


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
    n_mul = 4

    n_notes = int(n_measures * n_notes_per_measure * n_mul)
    p = [0.0005, 0.01, 0.1, 0.3, 0.0, 0.3, 0.1, 0.01, 0.0005]
    p = p / np.sum(p)
    steps = np.random.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4],
                             n_notes - 1, p=p)
    notes = np.array(scale.generate(4, 6))
    rw = elastic_bounded_random_walk(steps, np.random.randint(0, len(notes)), 0, len(notes))
    notes = notes[rw.astype(int)]

    cisd = ChordInScaleDefinition(scale)

    # TODO: use proper measures, instead of one big measure with all notes
    measure = Measure(tempo, signature)
    for index, note in enumerate(notes):
        vel = 2 if (index % 8) in [0, 3, 5] else 1.2
        cnotes = cisd.generate_chord(note)
        cnotes.notes[1].increment(0)
        for n in cnotes.notes[0:1]:
            measure.add_note(n, index * 1 / n_mul, 1 / n_mul, vel)
    track = Track([measure])

    return track


def generate_dataset(n_measures,
                     tempo=Tempo(120),
                     scale=GenericScale('C', [0, 2, 3, 5, 7, 8, 10]),
                     sampling_info=SamplingInfo(44100)):

    signature = Signature(4, 4)
    n_notes_per_measure = 4

    bass_instrument = make_bass_instrument(sampling_info)
    lead_instrument = make_lead_instrument(sampling_info)
    chord_instrument = make_accomp_instrument(sampling_info)

    chord_track = generate_chord_track(scale, tempo, signature, n_measures)
    y_chord = chord_instrument.generate_track(chord_track)

    lead_track = generate_lead_track(scale, tempo, signature, n_measures, n_notes_per_measure)
    y_lead = lead_instrument.generate_track(lead_track)

    bass_track = generate_bass_track(scale, tempo, signature, n_measures)
    y_bass = bass_instrument.generate_track(bass_track)

    mix = mixdown([y_bass, y_chord, y_lead])

    return [bass_track, chord_track, lead_track], [y_bass, y_chord, y_lead], mix