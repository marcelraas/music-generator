from music_generator.synthesizer.instrument import Instrument
from music_generator.synthesizer.oscillators import AliasingSquareOscillator
from music_generator.signalproc.signalproc import SamplingInfo
from music_generator.music.songs import vader_jacob

from music_generator.analysis.play import play_array


def test_generation():

    sampling_info = SamplingInfo(88200)
    instrument = Instrument(AliasingSquareOscillator(sampling_info))

    vj = vader_jacob()

    y = instrument.generate_track(vj)

    # Interactively you can listen to it, bit annoying to have to wait for it during testing
    # play_array(y, sampling_info.sample_rate)

    # play_array(apply_filter(y, sampling_info, 5e3))


