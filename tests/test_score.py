from music_generator.music.notes import Note
from music_generator.music.timing import Tempo, Signature, Duration
from music_generator.music.score import Measure, Score
from music_generator.music.songs import vader_jacob


def test_bar():
    bar = Measure(Tempo(120), Signature(3, 4))
    assert bar.total_time().seconds == 1.5


def test_measure():

    measure = Measure(Tempo(120), Signature(4, 4))

    measure.add_note(Note('C', 3), 0, 1)
    measure.add_note(Note('D', 3), 1, 1)
    measure.add_note(Note('E', 3), 2, 1)
    measure.add_note(Note('C', 3), 3, 1)

    assert len(measure.notes) == 4


def test_track():

    track = vader_jacob()

    assert len(track.measures) == 8
    assert len(track.measures[0].notes) == 4
    assert len(track.measures[2].notes) == 3
    assert len(track.measures[4].notes) == 6
    assert len(track.measures[6].notes) == 3


def test_measure_note_generate():
    measure = Measure(Tempo(120), Signature(4, 4))
    measure.add_note(Note('C#', 3), 0, 1)
    measure.add_note(Note('D', 3), 1, 1)
    measure.add_note(Note('E', 3), 2, 1)
    measure.add_note(Note('C#', 3), 3, 1)
    result = measure.generate_notes(Duration(1.5))
    assert result[0].offset.seconds == (measure.notes[0].offset + Duration(1.5)).seconds
    pass


def test_track_generate_notes():

    track = vader_jacob()
    notes = track.generate_notes()

    assert len(notes) == 32
    assert notes[31].offset.seconds == 15

    assert True


def test_score():

    track = vader_jacob()
    score = Score()
    score.add_track('lead', track)


