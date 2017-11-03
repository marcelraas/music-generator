import numpy as np

from music_generator.musical.notes import init_notes_df
from music_generator.musical.notes import Note


def test_notes_df():
    df = init_notes_df()

    assert 'semi' in df
    assert 'symbol' in df
    assert 'sharp' in df
    assert 'flat' in df

    assert len(df) == 21


def test_notes():

    note = Note('A', 2)
    assert np.isclose(note.frequency(), 110)

    note = Note('C#', 5)
    assert np.isclose(note.frequency(), 1108.7305)

    assert Note('F#', 5).frequency() == Note('Gb', 5).frequency()

    pass

