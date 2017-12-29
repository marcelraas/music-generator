from music_generator.musical.notes import Note
from music_generator.musical.timing import Tempo, Signature
from music_generator.musical.score import Bar, Measure, Track


def vader_jacob():

    bar = Bar(Tempo(120), Signature(4, 4))

    theme1 = Measure(bar) \
        .add_note(Note('C', 3), 0, 1) \
        .add_note(Note('D', 3), 1, 1) \
        .add_note(Note('E', 3), 2, 1) \
        .add_note(Note('C', 3), 3, 1)

    theme2 = Measure(bar) \
        .add_note(Note('E', 3), 0, 1) \
        .add_note(Note('F', 3), 1, 1) \
        .add_note(Note('G', 3), 2, 2)

    theme3 = Measure(bar) \
        .add_note(Note('G', 3), 0, 0.5) \
        .add_note(Note('A', 3), 0.5, 0.5) \
        .add_note(Note('G', 3), 1, 0.5) \
        .add_note(Note('F', 3), 1.5, 0.5) \
        .add_note(Note('E', 3), 2, 1) \
        .add_note(Note('C', 3), 3, 1)

    theme4 = Measure(bar) \
        .add_note(Note('C', 3), 0, 1) \
        .add_note(Note('G', 2), 1, 1) \
        .add_note(Note('C', 3), 2, 2)

    track = Track([theme1] * 2 + [theme2] * 2 + [theme3] * 2 + [theme4] * 2)

    return track
