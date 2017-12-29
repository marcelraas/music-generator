from music_generator.musical.notes import Note
from music_generator.musical.timing import Signature, Tempo, Duration
from music_generator.synthesizer.instrument import Instrument

from copy import deepcopy
import numpy as np


class Bar(object):
    def __init__(self, tempo: Tempo, signature: Signature):
        """Create a musical bar

        Args:
            tempo: tempo
            signature: signature
        """
        self.tempo = tempo
        self.signature = signature

    def total_time(self):
        """Get total time

        Returns:
            Duration
        """
        return self.signature.get_num_quarter_notes() * self.tempo.quarter_note()

    def __repr__(self):
        return "{} at {}".format(str(self.signature), self.tempo)


class PositionedNote(object):
    def __init__(self, note: Note, position: Duration, duration: Duration):
        self.note = note
        self.position = position
        self.duration = duration

    def __repr__(self):
        return '{} at {} for {}'.format(self.note, self.position, self.duration)


class Measure(object):
    def __init__(self, bar):
        self.bar = bar
        self.notes = []

    def add_note(self, note: Note, position: float, duration: float):
        """Add a notes to a bar

        Args:
            note: notes to play
            position: position w.r.t. beats in the bar
            duration: duration w.r.t. beats in the bar (whole notes is 4 for 4/4)

        Returns:
            Measure: self
        """
        position = Duration.from_num_beats(position, self.bar.tempo)
        duration = Duration.from_num_beats(duration, self.bar.tempo)
        self.notes.append(PositionedNote(note, position, duration))
        return self


class Track(object):
    def __init__(self, measures, instrument=None):
        self.measures = measures
        self.instrument = instrument
        self.velocity = 0.2

    def generate_audio(self, pcm=None, sample_rate=44100):
        assert isinstance(self.instrument, Instrument)

        positioned_notes = self.generate_notes()

        for note in positioned_notes:
            assert False
            # pcm = positioned_mix(pcm, note.position.samples(sample_rate), self.instrument.generate_note(note.note, note.duration, self.velocity))

        return pcm

    def generate_notes(self):

        # TODO: pretty UGLY
        notes = []
        offset = Duration(0)
        for measure in self.measures:
            new_notes = []
            for note in measure.notes:
                new_note = deepcopy(note)
                new_note.position += offset
                new_notes.append(new_note)
            notes += new_notes
            offset += measure.bar.total_time()

        return notes


class Score(object):
    def __init__(self):
        self.tracks = dict()

    def add_track(self, name, track):
        self.tracks[name] = track

    def get_track(self, name):

        if name not in self.tracks:
            return IndexError('{} not found in tracks'.format(name))

        return self.tracks[name]
