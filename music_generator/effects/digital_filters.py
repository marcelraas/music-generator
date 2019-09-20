"""Digital filters

Based on http://research.spa.aalto.fi/publications/theses/vaananen_mst.pdf
"""

import numpy as np

from music_generator.signalproc import signalproc


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


class IirFilter(object):
    def __init__(self, gain_coefs_fwd, delays_fwd,
                 gain_coefs_bwd, delays_bwd):

        self.bwd_loop_idx = np.argsort(delays_bwd)[::-1]

        self.gain_coefs_fwd = gain_coefs_fwd
        self.delays_fwd = delays_fwd

        self.delays_bwd = np.array(delays_bwd)[self.bwd_loop_idx]
        self.gain_coefs_bwd = np.array(gain_coefs_bwd)[self.bwd_loop_idx]

    def apply(self, x):

        result = np.array(x)

        for gc, delay in zip(self.gain_coefs_fwd, self.delays_fwd):
            x_ = x * gc
            result = signalproc.mix_at(result, x_, delay)

        for i in range(len(result)):
            for gc, delay in zip(self.gain_coefs_bwd, self.delays_bwd):
                delayed_i = i - delay
                if delayed_i >= 0:
                    result[i] = result[i] + gc * result[delayed_i]

        return result


class CombAllPassReverb(object):

    def __init__(self, gain_coefs, delays):

        self.delays = np.array(delays)
        self.gain_coefs = np.array(gain_coefs)

    def apply(self, x):

        result = np.zeros_like(x)
        v = np.zeros_like(result)
        w = np.zeros_like(result)

        for idx in range(len(result)):

            for g, d in zip(self.gain_coefs, self.delays):

                idx_for_w = int(idx - d)
                if idx_for_w >= 0:
                    w[idx] = v[idx_for_w]
                else:
                    w[idx] = 0

                v[idx] = g*w[idx] + x[idx]
                result[idx] = -g*v[idx] + w[idx]

        return result

