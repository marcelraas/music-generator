import numpy as np

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


def x_fade_profile(batch_dim):
    x = np.arange(batch_dim)
    return 1 - abs(x - (batch_dim / 2)) / (batch_dim / 2)


def model_predict(model, input_track, sample_size):
    dim = sample_size
    n_batches = int(len(input_track) / dim) - 1
    pred_batches = input_track[0:n_batches * dim].reshape((-1, dim))

    pred_batches_shifted = input_track[dim // 2:n_batches * dim + dim // 2].reshape((-1, dim))

    xfp = x_fade_profile(dim)

    x0 = np.array([xfp * batch for batch in model.predict(pred_batches)]).reshape(-1)
    x1 = np.array([xfp * batch for batch in model.predict(pred_batches_shifted)]).reshape(-1)

    return mix_at(x0, x1, dim // 2)
