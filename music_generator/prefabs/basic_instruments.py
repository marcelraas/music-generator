from music_generator.synthesizer.instrument import Instrument
from music_generator.synthesizer.oscillators import SquareOscillator, LinearAdsrGenerator, FilteredOscillator


def make_bass_instrument(sampling_info):
    osc = SquareOscillator(sampling_info)
    base_gen = LinearAdsrGenerator(0.1e-3, 2, 0.01, 0.01, osc)
    generator = FilteredOscillator(sampling_info,
                                   1000,
                                   filter_type="lowpass",
                                   base_generator=base_gen,
                                   order=1)
    bass_instrument = Instrument(generator)
    bass_instrument.velocity = 0.1
    return bass_instrument


def make_lead_instrument(sampling_info):
    osc = SquareOscillator(sampling_info)
    lead_base_gen = LinearAdsrGenerator(1e-3, 100e-3, 0.3, 0.1, osc)
    lead_generator = FilteredOscillator(sampling_info,
                                        15000,
                                        filter_type="lowpass",
                                        base_generator=lead_base_gen,
                                        order=1)
    lead_generator.couple_velocity = 0.5
    lead_instrument = Instrument(lead_generator)
    lead_instrument.velocity = 0.05
    return lead_instrument


def make_accomp_instrument(sampling_info):
    osc = SquareOscillator(sampling_info)
    chord_base_gen = LinearAdsrGenerator(200e-3, 0.1e-6, 1.0, 500e-3, osc)
    chord_generator = FilteredOscillator(sampling_info, 800, "lowpass", chord_base_gen, order=1)
    chord_instrument = Instrument(chord_generator)
    chord_instrument.velocity = 0.05
    return chord_instrument