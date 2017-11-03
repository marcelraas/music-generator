import sys

from argparse import ArgumentParser

from music_generator.analysis.play import play_array
from music_generator.basic.random import monophonic_random
from music_generator.basic.random import monophonic_notes
from music_generator.synthesizer.oscillators import SquareOscillator
from music_generator.synthesizer.oscillators import SineOscillator, AliasingSquareOscillator


def parse_args():
    arg_parser = ArgumentParser(description='Generate notes')

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

    y = monophonic_notes(n_notes, note_duration, 0.2, AliasingSquareOscillator(sample_rate))

    y = y[0:int(length * sample_rate)]

    play_array(y)

    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(**vars(args)))

