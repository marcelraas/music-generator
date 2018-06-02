from music_generator.basic import random_lead
from music_generator.musical.scales import GenericScale


def test_generate_chords():
    scale = GenericScale('C', [0, 2, 3, 5, 7, 8, 10])
    chord_track = random_lead.generate_chords(scale, 4, 4, 32)

    pass