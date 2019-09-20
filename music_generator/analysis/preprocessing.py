import numpy as np
import scipy.io.wavfile as wf
from scipy.fftpack import rfft

from music_generator.basic.utils import parallel_apply_along_axis
from music_generator.signalproc.signalproc import mix_at


def read_wave_file(filename, channel=0):
    sampling_rate, x = wf.read(filename)
    norm = 1.0
    if x.dtype == np.int8:
        norm = 2**(8-1)
    elif x.dtype == np.int16:
        norm = 2 ** (16 - 1)
    elif x.dtype == np.int32:
        norm = 2 ** (32 - 1)
    return sampling_rate, x[:, channel] / norm


def store_wave_file(filename, sampling_rate, data):
    wf.write(filename, sampling_rate, data)


def create_batches(data, batch_size, step):
    """Create batches with fixed size from input

    Args:
        data (np.array):
            input data: 1-d array

        batch_size (int):
            size of batch in number samples

        step (int):
            number of samples to step in order to begin a new one. If step is
            smaller than the batch size, subsequent samples in a batch will be
            overlapping.

    Returns:
        list[np.array]:
            batches
    """

    batch_ix = np.arange(0, len(data) - batch_size, step)
    batches = [data[ix:ix + batch_size] for ix in batch_ix]

    return batches


def batches_to_array(batches, step):

    batch_size = batches.shape[1]
    half_size = batch_size // 2

    batches = [b * (1 - np.abs(np.linspace(-half_size, half_size, num=batch_size)) / half_size) for b in batches]

    n_samples = len(batches) * step + batch_size

    result = np.zeros(n_samples)

    for i, b in enumerate(batches):
        result[(i*step):(i*step + batch_size)] += b

    return result


def clip_to_same_length(arrays):
    min_size = np.min([len(arr) for arr in arrays])
    return np.array([arr[0:min_size] for arr in arrays])


def combine_datasets(list_of_datasets):
    tuple_of_audio_tracks = tuple(clip_to_same_length(el[1]) for el in list_of_datasets)
    max_lens = [at.shape[1] for at in tuple_of_audio_tracks]
    tuple_of_mixes = tuple(np.array(el[2][0:ml]) for el, ml in zip(list_of_datasets, max_lens))
    audio_tracks = np.concatenate(tuple_of_audio_tracks, axis=1)
    mix = np.concatenate(tuple_of_mixes)

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
