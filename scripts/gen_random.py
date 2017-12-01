import sys

from argparse import ArgumentParser

from music_generator.analysis.play import play_array
from music_generator.basic.random import monophonic_random
from music_generator.basic.random import monophonic_scale
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.synthesizer.oscillators import SineOscillator, AliasingSquareOscillator
from music_generator.musical.scales import GenericScale


def parse_args():
    arg_parser = ArgumentParser(description='Generate steps')

    arg_parser.add_argument('--length',
                            metavar='<LENGTH>',
                            dest='length',
                            default=30,
                            type=float,
                            help='length in seconds')

    arg_parser.add_argument('--note_duration',
                            metavar='<NOTE_DURATION>',
                            dest='note_duration',
                            default=0.2,
                            type=float,
                            help='note duration')

    return arg_parser.parse_args()


def main(length, note_duration):
    """Main function

    Args:
        length (float): length in seconds
        note_duration (float): duration of a single note in seconds

    Returns:
        int: program exit-code
    """

    sample_rate = 88200

    n_notes = int(length / note_duration) + 1

    y = monophonic_scale(n_notes,
                         note_duration,
                         0.2,
                         GenericScale('C', [0, 2, 4, 5, 7, 9, 11]),
                         SineOscillator(sample_rate))

    y = y[0:int(length * sample_rate)]

    play_array(y)

    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(**vars(args)))

