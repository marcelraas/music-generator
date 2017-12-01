from music_generator.musical.chords import Note
from music_generator.musical.chords import MajorChordDefinition


def test_major_chord():
    maj = MajorChordDefinition()
    maj.generate_chord(Note('C', 3))
    assert True

