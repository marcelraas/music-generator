from music_generator.musical.notes import Note

import copy


class ChordDefinition(object):
    def __init__(self, intervals):
        self.intervals = intervals

    def generate_chord(self, root: Note):
        return Chord([copy.copy(root).increment(iv) for iv in self.intervals])


class MajorChordDefinition(ChordDefinition):
    def __init__(self):
        ChordDefinition.__init__(self, [0, 4, 7])


class Chord(object):
    def __init__(self, notes):
        self.notes = notes

    def __repr__(self):
        return str(self.notes)
