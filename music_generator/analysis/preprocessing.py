import numpy as np
from scipy.fftpack import rfft, irfft

from music_generator.basic.utils import parallel_apply_along_axis

from music_generator.basic.signalproc import mix_at


def combine_datasets(ds1, ds2):
    print("WARNING: not combining the score tracks")
    audio_tracks = [np.concatenate((x1, x2)) for x1, x2 in zip(ds1[1], ds2[1])]
    mix = np.concatenate((ds1[2], ds2[2]))

    return audio_tracks, mix


def create_training_data_set(n_samples, fragment_length, input_track, target_track):
    max_index = min(len(input_track), len(target_track))
    max_start_index = max_index - fragment_length

    # Selection range
    selection_ranges = np.random.randint(0, max_start_index, n_samples)
    selection_ranges = [{'begin': x, 'end': x + fragment_length} for x in selection_ranges]

    x = np.array([input_track[sr['begin']:sr['end']] for sr in selection_ranges])
    y = np.array([target_track[sr['begin']:sr['end']] for sr in selection_ranges])

    return x, y


def apply_fourier_on_dataset(dataset: np.array):
    return np.apply_along_axis(rfft, 0, dataset)


def x_fade_profile(batch_dim):
    x = np.arange(batch_dim)
    return 1 - abs(x - (batch_dim / 2)) / (batch_dim / 2)


def decoder_predict(decoder_model, encoded_x, trans_bw):
    return parallel_apply_along_axis(trans_bw, 0, decoder_model.predict(encoded_x)).reshape(-1)


def apply_fourier_on_input(input_track, window_size):
    n_batches = int(len(input_track) / window_size)
    batches = input_track[0:n_batches*window_size].reshape((-1, window_size))
    return parallel_apply_along_axis(rfft, 0, batches)


def model_predict(model, input_track, sample_size, trans_fw=None, trans_bw=None):
    dim = sample_size
    n_batches = int(len(input_track) / dim) - 1

    pred_batches = input_track[0:n_batches * dim].reshape((-1, dim))
    pred_batches_shifted = input_track[dim // 2:n_batches * dim + dim // 2].reshape((-1, dim))

    print("FFT transforming...")

    if trans_fw is not None:
        pred_batches, pred_batches_shifted = map(lambda x: parallel_apply_along_axis(trans_fw, 0, x),
                                                 (pred_batches, pred_batches_shifted))

    if trans_bw is None:
        trans_bw = lambda x: x

    xfp = x_fade_profile(dim)

    print("Predicting and transforming...")

    pred_batches, pred_batches_shifted = map(lambda x: parallel_apply_along_axis(trans_bw, 0, model.predict(x)),
                                             (pred_batches, pred_batches_shifted))

    print("Applying x-fade and mixing...")
    x0 = np.array([xfp * batch for batch in pred_batches]).reshape(-1)
    x1 = np.array([xfp * batch for batch in pred_batches_shifted]).reshape(-1)

    return mix_at(x0, x1, dim // 2)
