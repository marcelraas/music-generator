from music_generator.music.notes import Note
from music_generator.music.chords import Chord
from music_generator.music.timing import Duration, Signature, Tempo
from music_generator.music.score import Track, PositionedNote, Measure
from music_generator.synthesizer.oscillators import Generator
from music_generator.signalproc.signalproc import mix_at
from music_generator.synthesizer.oscillators import SquareOscillator, LinearAdsrGenerator, FilteredOscillator

from music_generator.music.utils import get_max_duration

import numpy as np


class Instrument(object):

    def __init__(self, generator: Generator):
        self.generator = generator
        self.velocity = 0.2

    def generate_note(self, note: Note, duration: Duration = Duration(1), velocity: float = 1):
        return self.generator.generate_note(note, duration.seconds, amplitude=velocity, phase=0)

    def generate_track(self, track: Track):

        positioned_notes = np.array(track.generate_notes())
        max_duration = get_max_duration(positioned_notes)

        pcm = self.generator.sampling_info.generate_silence(max_duration.seconds)

        for note in positioned_notes:
            assert isinstance(note, PositionedNote)
            y = self.generate_note(note.note, note.duration, self.velocity * note.velocity)

            # Note: variable pcm is updated in max_at method
            pcm = mix_at(pcm, y, note.offset.samples(self.generator.sampling_info.sample_rate))

        return pcm

    def generate_chord(self, chord: Chord, time: Duration):

        tempo = Tempo(120)
        measure = Measure(tempo, Signature(4, 4))

        for n in chord.notes:
            measure.add_note(n, 0, duration=time.beats(tempo))

        track = Track([measure])

        return self.generate_track(track)





def make_lead_instrument(sampling_info):
    osc = SquareOscillator(sampling_info)
    lead_base_gen = LinearAdsrGenerator(1e-3, 100e-3, 0.3, 0.1, osc)
    lead_generator = FilteredOscillator(sampling_info,
                                        7000,
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
