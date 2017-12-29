from music_generator.musical.notes import Note
from music_generator.musical.timing import Duration
from music_generator.synthesizer.oscillators import Generator


class Instrument(object):

    def __init__(self, generator: Generator):
        self.generator = generator

    def generate_note(self, note: Note, duration: Duration, velocity: float):
        return self.generator.generate_note(note, duration.seconds(), amplitude=velocity, phase=0)
