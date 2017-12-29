from music_generator.synthesizer.oscillators import AdditiveOscillator
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.basic.signalproc import SamplingInfo


def test_additive_osc():

    additive = AdditiveOscillator(SamplingInfo(44100), [1, 0.5, 0.25, 0.125])

    fx = additive.generate(0.5, 1, 440, 0)


def test_square_osc():

    square = SquareOscillator(SamplingInfo(44100))
    fx = square.generate(0.5, 1, 440, 0)

    pass

