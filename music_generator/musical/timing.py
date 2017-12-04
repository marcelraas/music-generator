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
            Duration instance
        """
        return cls(quarters * tempo.quarter_note().seconds)

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


class Tempo(object):
    def __init__(self, bpm: float):
        """Define a tempo by beats per minute

        A beat corresponds to a quarter note.

        Args:
            bpm: beats per minute, should be larger than 0
        """
        if bpm <= 0:
            raise ValueError('bpm (beats per minute) should be larger than 0')
        self.bpm = bpm

    def quarter_note(self):
        """Get length of a quarter note in seconds

        Returns:
            Duration: duration object
        """
        return Duration(60. / self.bpm)


class Signature(object):
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        return '{}/{}'.format(self.numerator, self.denominator)


