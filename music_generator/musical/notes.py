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

    return notes.reset_index(drop=True)


NOTES_DF = init_notes_df()


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

    def calc_frequency(self, symbol, octave):

        semi_steps = self.notes_df.loc[symbol].semi
        semi_steps += (octave - 4) * 12

        return self.a4_freq * self.semi_tone_ratio ** semi_steps


EQUAL_TEMPERED_A4_440 = EqualTempered(440)


class Note(object):

    def __init__(self, symbol, octave, tuning=EQUAL_TEMPERED_A4_440):
        self.octave = octave
        self.symbol = symbol
        self.tuning = tuning

    def frequency(self):
        return self.tuning.calc_frequency(self.symbol, self.octave)
