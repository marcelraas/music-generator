"""Module for notes and frequencies

Definitions:
    * Symbol: the note's symbolic name (e.g. C, F#)

Conventions:
    * In a sequence of notes, octaves increment at each following C, i.e. A#2, B2, C3, C#3, etc.
    * Only sharp symbols are allowed in note symbolic notation, i.e. use C# not Db
    * Symbols are written in upper case
"""

from copy import deepcopy

BASE_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
_A4_BASE = 57
_A4_TUNING = 440


class Note(object):
    def __init__(self, symbol: str, octave: int):
        self.semi_from_c0 = self.calc_semi_from_c0(symbol, octave)

    def get_octave(self):
        """Returns octave"""
        return int(self.semi_from_c0 / 12)

    def get_symbol(self):
        """Gets symbol"""
        return BASE_NOTES[self.semi_from_c0 % 12]

    def get_semi_from_a4(self):
        """Get distance in semitones from A4"""
        return self.semi_from_c0 - _A4_BASE

    def increment(self, semitones):
        """Increment notes with this number of semitones"""
        self.semi_from_c0 += semitones
        return self

    def frequency(self):
        """Calculate frequency of notes"""
        return (2 ** (self.get_semi_from_a4()/12.)) * _A4_TUNING

    @staticmethod
    def calc_semi_from_c0(symbol: str, octave: int):
        """Calculate semitones from c0

        Args:
            symbol: symbol of notes (e.g. C, C#, etc., do not use flats)
            octave: octave of notes (see doc on top of module)
        """
        return BASE_NOTES.index(symbol) + octave * 12

    def __repr__(self):
        return '{}{}'.format(self.get_symbol(), self.get_octave())

    def clone(self):
        """Create a clone of itself

        Returns:
            Note: clone
        """
        return deepcopy(self)




