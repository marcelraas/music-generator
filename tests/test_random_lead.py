from music_generator.basic import random_lead
from music_generator.musical.scales import GenericScale
from music_generator.musical.chords import Chord


def test_generate_chords():
    scale = GenericScale('C', [0, 2, 3, 5, 7, 8, 10])
    chord_track = random_lead.generate_chords(scale, 32, 4, 4)

    assert len(chord_track) == 32
    assert type(chord_track[0]) == Chord

    pass


