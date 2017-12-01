from music_generator.musical.notes import Note
from music_generator.musical.scales import GenericScale

import copy


class ChordDefinition(object):
    def __init__(self, intervals):
        self.intervals = intervals

    def generate_chord(self, root: Note):
        return Chord([copy.copy(root).increment(iv) for iv in self.intervals])

    def aug(self):
        self.intervals[self.intervals.index(7)] += 1
        return self

    def dim(self):
        self.intervals[self.intervals.index(7)] -= 1
        return self


class MajorChordDefinition(ChordDefinition):
    def __init__(self):
        ChordDefinition.__init__(self, [0, 4, 7])


class MinorChordDefinition(ChordDefinition):
    def __init__(self):
        ChordDefinition.__init__(self, [0, 3, 7])


class ChordInScaleDefinition(object):
    def __init__(self, scale):
        self.scale = scale

    def generate_chord(self, root: Note):
        candidate = MajorChordDefinition().generate_chord(root)
        if candidate.is_in_scale(self.scale):
            return candidate

        candidate = MinorChordDefinition().generate_chord(root)
        if candidate.is_in_scale(self.scale):
            return candidate

        candidate = MajorChordDefinition().aug().generate_chord(root)
        if candidate.is_in_scale(self.scale):
            return candidate

        candidate = MinorChordDefinition().aug().generate_chord(root)
        if candidate.is_in_scale(self.scale):
            return candidate

        candidate = MajorChordDefinition().dim().generate_chord(root)
        if candidate.is_in_scale(self.scale):
            return candidate

        candidate = MinorChordDefinition().dim().generate_chord(root)
        if candidate.is_in_scale(self.scale):
            return candidate

        assert False, "Can happen though"


class Chord(object):
    def __init__(self, notes):
        self.notes = notes

    def __repr__(self):
        return str(self.notes)

    def get_symbols(self):
        return [x.get_symbol() for x in self.notes]

    def is_in_scale(self, scale: GenericScale):
        symbols_in_chord = self.get_symbols()
        symbols_in_scale = scale.get_symbols()

        if set(symbols_in_chord) - set(symbols_in_scale) == set():
            return True
        else:
            return False


