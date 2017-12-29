from music_generator.musical.timing import Signature
from music_generator.musical.timing import Tempo
from music_generator.musical.timing import Duration


def test_signature():
    signature = Signature(4, 4)
    assert str(signature) == '4/4'

    signature = Signature(7, 8)
    assert str(signature) == '7/8'


def test_tempo():
    tempo = Tempo(120)
    assert tempo.quarter_note().seconds == 0.5


def test_duration():
    duration = Duration.from_num_beats(2, Tempo(120))
    assert duration.seconds == 1

    tempo = Tempo(613)
    duration = Duration.from_num_beats(0.5, tempo)
    assert duration.beats(tempo) == 0.5

    assert Duration.from_num_beats(1, Tempo(120)).samples(44100) == 22050


def test_duration_operators():
    duration = Duration.from_num_beats(2, Tempo(120))
    assert duration.seconds == 1

    assert (duration * 2).seconds == 2
    assert duration.seconds == 1

    assert (2 * duration).seconds == 2
    assert duration.seconds == 1

    assert (duration + Duration(1)).seconds == 2
    assert duration.seconds == 1

    pass
