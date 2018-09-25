from scipy.io import wavfile
import logging
import os
import numpy as np
from music_generator.analysis import preprocessing


class FullMixToFilterDataSet(object):

    def __init__(self, full_mix_files, filtered_files, base_dir=None):

        self._full_mix_files = full_mix_files
        self._filtered_files = filtered_files
        self.base_dir = base_dir

        self._load()

    def _load(self):

        self.full_mix = self.load_and_concatenate(self._full_mix_files)
        self.filtered = self.load_and_concatenate(self._filtered_files)

    def get_full_filename(self, f):
        if self.base_dir is not None:
            return os.path.join(self.base_dir, f)
        else:
            return f

    def load_and_concatenate(self, files):

        def get_data_single(f):
            sr, data = wavfile.read(self.get_full_filename(f))
            if sr != 44100:
                logging.warning("Sample rate != 44100, I have not tested with this")
            return data / 2**16

        return np.concatenate(tuple([get_data_single(f) for f in files]), axis=0)


class JamDataSet(object):

    def __init__(self,
                 fragment_length,
                 n_samples_train=4000,
                 n_samples_test=1000,
                 data_dir="../data/"):
        self.data_dir = data_dir

        self._train_data = FullMixToFilterDataSet(
            ['full-mix-jam1-01.wav',
             'full-mix-jam1-02.wav',
             'full-mix-jam1-03.wav',
             'full-mix-jam1-04.wav',
             'full-mix-jam1-05.wav',
             'full-mix-jam1-06.wav',
             'full-mix-jam1-07.wav',
             'full-mix-jam1-09.wav',
             'full-mix-jam2.wav',
             'full-mix-jam3.wav',
             'full-mix-jam6.wav',
             'full-mix-jam7.wav'],
            ['only-guitar-jam1-01.wav',
             'only-guitar-jam1-02.wav',
             'only-guitar-jam1-03.wav',
             'only-guitar-jam1-04.wav',
             'only-guitar-jam1-05.wav',
             'only-guitar-jam1-06.wav',
             'only-guitar-jam1-07.wav',
             'only-guitar-jam1-09.wav',
             'only-guitar-jam2.wav',
             'only-guitar-jam3.wav',
             'only-guitar-jam6.wav',
             'only-guitar-jam7.wav'],
            base_dir=data_dir)

        self._test_data = FullMixToFilterDataSet(
            ['full-mix.wav'],
            ['only-guitar.wav'],
            base_dir=data_dir)

        self.x_train, self.y_train = \
            preprocessing.create_training_data_set(n_samples_train,
                                                   fragment_length,
                                                   self._train_data.full_mix,
                                                   self._train_data.filtered)

        self.x_test, self.y_test = \
            preprocessing.create_training_data_set(n_samples_test,
                                                   fragment_length,
                                                   self._test_data.full_mix,
                                                   self._test_data.filtered)

