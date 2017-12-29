from music_generator.musical.notes import Note
from music_generator.musical.timing import Tempo, Signature, Duration
from music_generator.musical.score import Measure
from music_generator.musical.utils import get_max_duration


def test_max_duration():
    measure = Measure(Tempo(120), Signature(4, 4))
    measure.add_note(Note('C#', 3), 0, 1)
    measure.add_note(Note('F', 3), 2, 5)
    measure.add_note(Note('D', 3), 1, 1)
    measure.add_note(Note('E', 3), 2, 1)
    measure.add_note(Note('C#', 3), 3, 1)

    max_duration = get_max_duration(measure.generate_notes(Duration(1.5)))

    assert max_duration.seconds == 5.0
