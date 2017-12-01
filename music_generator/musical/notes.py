BASE_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
_A4_BASE = 57


class Note(object):
    def __init__(self, symbol: str, octave: int):
        self.semi_from_c0 = self.calc_semi_from_c0(symbol, octave)

    def get_octave(self):
        return int(self.semi_from_c0 / 12)

    def get_symbol(self):
        return BASE_NOTES[self.semi_from_c0 % 12]

    def get_semi_from_a4(self):
        return self.semi_from_c0 - _A4_BASE

    def increment(self, semitones):
        self.semi_from_c0 += semitones
        return self

    def frequency(self):
        return (2 ** (self.get_semi_from_a4()/12.)) * 440

    @staticmethod
    def calc_semi_from_c0(symbol, octave):
        return BASE_NOTES.index(symbol) + octave * 12

    def __repr__(self):
        return '{}{}'.format(self.get_symbol(), self.get_octave())




