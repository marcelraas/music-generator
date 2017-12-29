from music_generator.musical.notes import Note
from music_generator.musical.timing import Tempo, Signature, Duration
from music_generator.musical.score import Bar, Measure, Score
from music_generator.musical.songs import vader_jacob


def test_bar():
    bar = Bar(Tempo(120), Signature(3, 4))

    assert bar.total_time().seconds == 1.5


def test_measure():

    bar = Bar(Tempo(120), Signature(4, 4))

    measure = Measure(bar)

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


def test_track_generate_notes():

    track = vader_jacob()
    notes = track.generate_notes()

    assert len(notes) == 32
    assert notes[31].position.seconds == 15

    assert True


def test_score():

    track = vader_jacob()
    score = Score()
    score.add_track('lead', track)


