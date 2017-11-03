import numpy as np
import pandas as pd


def init_notes_df():
    notes = pd.DataFrame({'symbol': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                          'semi': [0, 2, 3, 5, 7, 8, 10]})

    notes['sharp'] = 0
    notes['flat'] = 0

    notes = pd.concat(
        [notes,
         notes.assign(semi=lambda x: x.semi + 1)
             .assign(symbol=lambda x: x.symbol + '#')
             .assign(sharp=1),
         notes.assign(semi=lambda x: x.semi - 1)
             .assign(symbol=lambda x: x.symbol + 'b')
             .assign(flat=1)])

    notes = notes[~notes.symbol.isin(['B#', 'Cb', 'E#', 'Fb'])]

    return notes.reset_index()


NOTES_DF = init_notes_df()
NOTES_SHARP = NOTES_DF[NOTES_DF.flat == 0]
NOTES_FLAT = NOTES_DF[NOTES_DF.sharp == 0]


def semi_from_a4(symbol, octave):
    semi_steps = NOTES_DF.set_index('symbol').loc[symbol].semi
    semi_steps += (octave - 4) * 12
    return semi_steps


class Tuning(object):
    def __init__(self):
        pass

    def calc_frequency(self):
        pass


class EqualTempered(object):
    def __init__(self, a4_frequency):

        self.notes_df = NOTES_DF.set_index('symbol')
        self.a4_freq = a4_frequency
        self.semi_tone_ratio = 2**(1/12)

    def calc_frequency(self, semi_from_a4):
        return self.a4_freq * self.semi_tone_ratio ** semi_from_a4


EQUAL_TEMPERED_A4_440 = EqualTempered(440)


class Note(object):

    def __init__(self, symbol, octave, tuning=EQUAL_TEMPERED_A4_440):
        self.tuning = tuning
        self.semi_from_a4 = semi_from_a4(symbol, octave)

    def frequency(self):
        return self.tuning.calc_frequency(self.semi_from_a4)

    def octave(self):
        return 4 + int((self.semi_from_a4 - 3) / 12)

    def symbol(self, sharp=True):
        semi = (self.semi_from_a4 % 12)
        df = NOTES_SHARP if sharp else NOTES_FLAT
        return df.set_index('semi').loc[semi].symbol

    def __repr__(self):
        return self.symbol() + str(self.octave())

