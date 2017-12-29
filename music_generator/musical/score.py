from music_generator.musical.notes import Note
from music_generator.musical.timing import Signature, Tempo, Duration

from copy import deepcopy
import numpy as np


class PositionedNote(object):
    def __init__(self, note: Note, offset: Duration, duration: Duration):
        self.note = note
        self.offset = offset
        self.duration = duration

    def __repr__(self):
        return '{} at {} for {}'.format(self.note, self.offset, self.duration)

    def add_offset(self, offset: Duration):
        """Add an offset to this note

        Args:
            offset: Duration

        Returns:
            PositionedNote: itself
        """
        self.offset += offset
        return self

    def get_moment_release(self):
        """Get moment of release of this note

        Returns:
            Duration
        """
        return self.offset + self.duration

    def clone(self):
        """Create a clone of itself

        Returns:
            PositionedNote: new instance
        """
        return deepcopy(self)


class Measure(object):
    def __init__(self, tempo: Tempo, signature: Signature):
        """Create a musical measure

        Args:
            tempo: tempo
            signature: signature
        """
        self.tempo = tempo
        self.signature = signature
        self.notes = []

    def total_time(self):
        """Get total time

        Returns:
            Duration
        """
        return self.signature.get_num_quarter_notes() * self.tempo.quarter_note()

    def add_note(self, note: Note, position: float, duration: float):
        """Add a note to a measure

        Args:
            note: notes to play
            position: position w.r.t. beats in the bar
            duration: duration w.r.t. beats in the bar (whole notes is 4 for 4/4)

        Returns:
            Measure: self
        """
        position = Duration.from_num_beats(position, self.tempo)
        duration = Duration.from_num_beats(duration, self.tempo)
        self.notes.append(PositionedNote(note, position, duration))
        return self

    def generate_notes(self, offset: Duration):
        """Generate notes with an additional offset (typically start of measure)

        Args:
            offset (Duration): start of measure

        Returns:
            list[PositionedNote]
        """
        return [note.clone().add_offset(offset) for note in self.notes]

    def __repr__(self):
        return "{} at {}".format(str(self.signature), self.tempo)


class Track(object):
    def __init__(self, measures):
        self.measures = measures

    def generate_notes(self):

        notes = []
        offset = Duration(0)
        for measure in self.measures:
            notes += measure.generate_notes(offset)
            offset += measure.total_time()

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
