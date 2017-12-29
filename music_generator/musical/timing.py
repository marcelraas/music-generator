from copy import deepcopy


class Duration(object):
    def __init__(self, seconds):
        self.seconds = seconds

    @classmethod
    def from_num_beats(cls, quarters: float, tempo):
        """Create a duration given number of quarter notes and a tempo

        Args:
            quarters: number (or fraction of quarter notes)
            tempo (Tempo): tempo

        Returns:
            Duration: new instance
        """
        return cls(quarters * tempo.quarter_note().seconds)

    def clone(self):
        """Creates a clone of itself

        Returns:
            Duration: new instance
        """
        return deepcopy(self)

    def samples(self, sample_rate: float):
        """Express duration in number of samples

        Args:
            sample_rate: sample rate

        Returns:
            float: number of samples
        """
        return self.seconds * sample_rate

    def beats(self, tempo):
        """Express duration in number of beats

        Args:
            tempo (Tempo): tempo object

        Returns:
            float: fraction of beats
        """
        return self.seconds * (tempo.bpm / 60.)

    def __repr__(self):
        return "{} s".format(self.seconds)

    def __iadd__(self, other):
        self.seconds += other.seconds
        return self

    def __add__(self, other):
        new = self.clone()
        new += other
        return new

    def __mul__(self, x: float):
        ret = self.clone()
        ret.seconds = self.seconds * x
        return ret

    __rmul__ = __mul__



class Tempo(object):
    def __init__(self, bpm: float):
        """Define a tempo by beats per minute

        A beat corresponds to a quarter notes.

        Args:
            bpm: beats per minute, should be larger than 0
        """
        if bpm <= 0:
            raise ValueError('bpm (beats per minute) should be larger than 0')
        self.bpm = bpm

    def quarter_note(self):
        """Get length of a quarter notes in seconds

        Returns:
            Duration: duration object
        """
        return Duration(60. / self.bpm)

    def __repr__(self):
        return "{:2.1f} bpm".format(self.bpm)


class Signature(object):
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def get_num_quarter_notes(self):
        """Get beat span expressed in quarter notes

        Examples:
            4/4 has 4 quarter notes
            3/4 has 3 quarter notes
            12/8 has 6 quarter notes
            15/16 has 3.75 quarter notes

        Returns:
            float
        """
        return self.numerator / (self.denominator / 4)

    def __repr__(self):
        return '{}/{}'.format(self.numerator, self.denominator)


