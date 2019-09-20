import sys

from argparse import ArgumentParser

from music_generator.analysis.play import play_array
from prefabs.random_walk_track import generate_dataset
from music_generator.music.timing import Tempo
from music_generator.music.scales import GenericScale
from music_generator.basic.signalproc import SamplingInfo


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

    score_tracks, audio_tracks, mix = generate_dataset(n_measures=16,
                                                       tempo=Tempo(100),
                                                       scale=GenericScale('E', [0, 2, 3, 5, 7, 8, 10]),
                                                       sampling_info=sampling_info)

    play_array(mix, sampling_info.sample_rate)

    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(**vars(args)))

