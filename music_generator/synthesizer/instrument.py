from music_generator.musical.notes import Note
from music_generator.musical.timing import Duration
from music_generator.musical.score import Track, PositionedNote
from music_generator.synthesizer.oscillators import Generator
from music_generator.basic.signalproc import SamplingInfo, mix_at

from music_generator.musical.utils import get_max_duration

import numpy as np


class Instrument(object):

    def __init__(self, generator: Generator):
        self.generator = generator
        self.velocity = 0.2

    def generate_note(self, note: Note, duration: Duration, velocity: float):
        return self.generator.generate_note(note, duration.seconds, amplitude=velocity, phase=0)

    def generate_track(self, track: Track):

        positioned_notes = np.array(track.generate_notes())
        max_duration = get_max_duration(positioned_notes)

        pcm = self.generator.sampling_info.generate_silence(max_duration.seconds)

        for note in positioned_notes:
            assert isinstance(note, PositionedNote)
            y = self.generate_note(note.note, note.duration, self.velocity * note.velocity)

            # Note, variable pcm is updated in max_at method
            mix_at(pcm, y, note.offset.samples(self.generator.sampling_info.sample_rate))

        return pcm