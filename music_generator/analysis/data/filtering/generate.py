
"""Regeneration of lead synth from combined signal"""
from functools import partial

from music_generator.signalproc.signalproc import SamplingInfo
from prefabs.random_walk_track import generate_dataset
from music_generator.music.timing import Tempo
from music_generator.music.scales import GenericScale
from music_generator.analysis import preprocessing

from music_generator.music import scales
from multiprocessing import Pool


def reshape_batches(x, batch_size, fragment_length):
    n_fragments = len(x) // fragment_length // batch_size
    x = x[:n_fragments * fragment_length * batch_size].reshape(-1, fragment_length)
    return x


def generate_synthetic_data(batch_size, fragment_length, sampling_rate):

    sampling_info = SamplingInfo(sampling_rate)

    all_roots = scales.chromatic_scale('C')

    # Generate in all keys
    roots = [n.get_symbol() for n in all_roots.generate(0, 1)]
    print(roots)

    with Pool(8) as pool:
        datasets_train = pool.map(partial(__generate_dataset_for_root, sampling_info=sampling_info), roots)
        datasets_test = pool.map(partial(__generate_dataset_for_root, sampling_info=sampling_info), roots)

    x_train, y_train = __process_dataset(datasets_train, batch_size, fragment_length)
    x_test, y_test = __process_dataset(datasets_test, batch_size, fragment_length)

    return x_train, y_train, x_test, y_test


def __generate_dataset_for_root(root, sampling_info: SamplingInfo):
    return generate_dataset(n_measures=32,
                            tempo=Tempo(120),
                            scale=GenericScale(root, [0, 2, 3, 5, 7, 8, 10]),
                            sampling_info=sampling_info)


def __process_dataset(dataset, batch_size, fragment_length):
    # Make one big data set and make sure data is of same size
    audio_tracks, mix = preprocessing.combine_datasets(dataset)

    x, y = mix, audio_tracks[2]

    x = reshape_batches(x, batch_size, fragment_length)
    y = reshape_batches(y, batch_size, fragment_length)

    return x, y


