from music_generator.musical.chords import Note
from music_generator.musical.chords import MajorChordDefinition
from music_generator.musical.chords import ChordInScaleDefinition
from music_generator.musical.scales import GenericScale

def test_major_chord():
    maj = MajorChordDefinition()
    maj.generate_chord(Note('C', 3))
    assert True


def test_in_scale():
    major_scale = GenericScale('C', [0, 2, 4, 5, 7, 9, 11])

    major_chord = MajorChordDefinition()
    chord = major_chord.generate_chord(Note('C', 3))
    assert chord.is_in_scale(major_scale)

    major_chord = MajorChordDefinition()
    chord = major_chord.generate_chord(Note('D', 3))
    assert not chord.is_in_scale(major_scale)


def test_chords_scale():
    major_scale = GenericScale('C', [0, 2, 4, 5, 7, 9, 11])

    csd = ChordInScaleDefinition(major_scale)
    csd.generate_chord(Note('C', 3))

    assert True

