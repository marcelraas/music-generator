import numpy as np

from music_generator.basic import signalproc

class FirFilter(object):
    def __init__(self, gain_coefs, delays=None):

        self.gain_coefs = np.array(gain_coefs)

        if delays is None:
            self.delays = np.arange(0, len(gain_coefs), 1)
        self.delays = np.array(delays)

    def apply(self, x):

        result = np.array(x)
        for gc, delay in zip(self.gain_coefs, self.delays):
            x_ = x * gc
            result = signalproc.mix_at(result, x_, delay)

        return result

