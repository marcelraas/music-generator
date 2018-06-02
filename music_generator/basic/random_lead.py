import numpy as np
from copy import copy

from music_generator.musical.timing import Signature, Tempo

from music_generator.basic.signalproc import SamplingInfo, mix_at
from music_generator.musical.scales import GenericScale
from music_generator.synthesizer.instrument import Instrument

from music_generator.synthesizer.oscillators import FilteredOscillator
from music_generator.synthesizer.oscillators import LinearAdsrGenerator
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.musical.chords import ChordInScaleDefinition
from music_generator.basic.utils import elastic_bounded_random_walk

from music_generator.musical.score import Track, Measure


def generate_chords(scale: GenericScale, num_measures=8, repeat=4, pattern=4):

    root_notes = scale.generate(3, 4)
    csd = ChordInScaleDefinition(scale)

    chords = []
    while True:

        new_pattern = []
        for pat in range(pattern):
            if pat == 0:
                new_pattern.append(csd.generate_chord(root_notes[0]))
            else:
                index = np.random.randint(len(root_notes))
                new_pattern.append(csd.generate_chord(root_notes[index]))

        for ii in range(repeat):
            for chord in new_pattern:
                chords.append(chord)
                if len(chords) == num_measures:
                    return chords
