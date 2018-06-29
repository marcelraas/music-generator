from music_generator.basic import random_lead
from music_generator.musical.scales import GenericScale
from music_generator.musical.chords import Chord
from music_generator.musical.timing import Signature, Tempo


def test_generate_chords():
    scale = GenericScale('C', [0, 2, 3, 5, 7, 8, 10])
    chord_track = random_lead.generate_chords(scale, 32, 4, 4)

    assert len(chord_track) == 32
    assert type(chord_track[0]) == Chord

    pass


def test_bass_with_chords():
    scale = GenericScale('C', [0, 2, 3, 5, 7, 8, 10])
    chords_track = random_lead.generate_chords(scale, 32, 4, 4)

    tempo = Tempo(120)
    signature = Signature(4, 4)

    trk_bass = random_lead.generate_bass(chords_track, signature, tempo)

    assert trk_bass.measures[0].str_summary() == \
        '4/4: (@120.0 bpm):' \
        '\nC1 at 0.0 s for 0.25 s\nC1 at 0.5 s for 0.25 s' \
        '\nC1 at 1.0 s for 0.25 s\nC1 at 1.5 s for 0.25 s'

    pass


def test_generate():
    music = random_lead.generate()

    pass
