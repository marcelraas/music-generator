"""Regeneration of lead synth from combined signal"""

#%%

from music_generator.basic.random import generate_dataset
from music_generator.basic.signalproc import SamplingInfo
from music_generator.musical.timing import Tempo
from music_generator.musical.scales import GenericScale
from music_generator.analysis.play import play_mono_as_stereo, play_array
from music_generator.basic.signalproc import mix_at
from music_generator.analysis import preprocessing

from music_generator.musical import scales
import numpy as np
from multiprocessing import Pool
from functools import partial

import matplotlib.pyplot as plt
from IPython.display import Audio

sr = 44100
sampling_info = SamplingInfo(sr)
n_samples = 4096
fragment_length = 4096


def generate_dataset_for_root(root):
    return generate_dataset(n_measures=32,
                            tempo=Tempo(120),
                            scale=GenericScale(root, [0, 2, 3, 5, 7, 8, 10]),
                            sampling_info=sampling_info)


def create_data_set(n_samples):

    # Generate in all keys
    all_roots = scales.chromatic_scale('C')
    roots = [n.get_symbol() for n in all_roots.generate(0, 1)]
    print(roots)

    with Pool(8) as pool:
        datasets = pool.map(generate_dataset_for_root, roots)

    # Make one big data set and make sure data is of same size
    audio_tracks, mix = preprocessing.combine_datasets(datasets)

    input_track = mix
    target_track = audio_tracks[2]

    return input_track, target_track


def create_data_set_guitar():

    from scipy.io.wavfile import read

    sr, full_mix = read("data/full-mix.wav", mmap=False)
    sr, only_guitar = read("data/only-guitar.wav", mmap=False)

    return full_mix / 2**16, only_guitar / 2**16


def x_fade_profile(batch_dim):
    x = np.arange(batch_dim)
    return 1 - abs(x - (batch_dim / 2)) / (batch_dim / 2)


def model_predict(model, input_track, fragment_length):
    dim = fragment_length
    n_batches = int(len(input_track) / dim) - 1
    pred_batches = input_track[0:n_batches * dim].reshape((-1, dim))

    pred_batches_shifted = input_track[dim // 2:n_batches * dim + dim // 2].reshape((-1, dim))

    xfp = x_fade_profile(dim)

    x0 = np.array([xfp * batch for batch in model.predict(pred_batches)]).reshape(-1)
    x1 = np.array([xfp * batch for batch in model.predict(pred_batches_shifted)]).reshape(-1)

    return mix_at(x0, x1, dim // 2)


#%%

input_track, target_track = create_data_set_guitar()

x, y = preprocessing.create_training_data_set(n_samples,
                                              fragment_length,
                                              input_track,
                                              target_track)


# %%

import tensorflow as tf

from music_generator.analysis import regen_models
import importlib

importlib.reload(regen_models)

model = regen_models.FftBranches(n_samples, learning_rate=1e-4).build_model()
model.summary()

#%%

model.fit(x, y, epochs=15, verbose=1)


#%%

start_sec, end_sec = 20, 60

pred = model_predict(model, input_track[start_sec*sr:end_sec*sr], fragment_length)
play_array(input_track[start_sec*sr:end_sec*sr])
play_array(pred)



#%%

x_pred = input_track[start_sec*sr:end_sec*sr]
x_pred = x_pred[:(len(x_pred) // fragment_length) * fragment_length]
x_pred = x_pred.reshape(-1, fragment_length)

y_pred = model.predict(x_pred)
play_array(y_pred)
