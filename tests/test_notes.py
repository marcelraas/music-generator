import numpy as np

from music_generator.music.notes import Note, _A4_BASE


def test_semitones():
    a4 = Note('A', 4)
    assert a4.get_semi_from_a4() == 0


def test_increment():
    a4 = Note('A', 4)
    assert a4.increment(1).get_symbol() == 'A#'


def test_increment_octave():
    a2 = Note('A#', 2)
    a2.increment(2)

    assert a2.get_symbol() == 'C'
    assert a2.get_octave() == 3


def test_frequency():
    a4 = Note('A', 4)
    a3 = Note('A', 3)
    assert a4.frequency() / 2 == a3.frequency()

