import sys

from argparse import ArgumentParser

from music_generator.analysis.play import play_array
from music_generator.basic.random import monophonic_scale
from music_generator.synthesizer.oscillators import AliasingSquareOscillator
from music_generator.musical.scales import GenericScale
from music_generator.basic.signalproc import SamplingInfo, apply_filter


def parse_args():
    arg_parser = ArgumentParser(description='Generate steps')

    arg_parser.add_argument('--length',
                            metavar='<LENGTH>',
                            dest='length',
                            default=10,
                            type=float,
                            help='length in seconds')

    arg_parser.add_argument('--note_duration',
                            metavar='<NOTE_DURATION>',
                            dest='note_duration',
                            default=0.10,
                            type=float,
                            help='notes duration')

    return arg_parser.parse_args()


def main(length, note_duration):
    """Main function

    Args:
        length (float): length in seconds
        note_duration (float): duration of a single notes in seconds

    Returns:
        int: program exit-code
    """

    sampling_info = SamplingInfo(88200)

    n_notes = int(length / note_duration) + 1
    n_notes = int(n_notes / 16) * 16

    y = monophonic_scale(n_notes,
                         note_duration,
                         0.1,
                         GenericScale('C', [0, 2, 4, 5, 7, 9, 11]),
                         base_osc=AliasingSquareOscillator,
                         sampling_info=sampling_info)

    play_array(y)

    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(**vars(args)))

