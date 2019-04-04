import tensorflow as tf
import numpy as np


class WaveExcerptGenerator(tf.keras.utils.Sequence):

    def __init__(self, wave_data, excerpt_length, n_samples, batch_size):
        super().__init__()

        self.data = wave_data
        self.n_samples = n_samples
        self.batch_size = batch_size
        self.excerpt_length = excerpt_length
        self.indices = None

        self.on_epoch_end()

    def __len__(self):

        return self.n_samples // self.batch_size

    def __getitem__(self, batch_index):

        i_start = batch_index * self.batch_size
        i_end = (batch_index + 1) * self.batch_size
        indices = self.indices[i_start:i_end]

        retval = np.empty([len(indices), self.excerpt_length])

        for ii, index in enumerate(indices):
            retval[ii, :] = self.data[index:index + self.excerpt_length]

        return retval

    def on_epoch_end(self):

        max_index = len(self.data) - self.excerpt_length - 1
        self.indices = np.random.randint(0, max_index, size=self.n_samples)


class WaveSequentialChopper(tf.keras.utils.Sequence):

    def __init__(self, data, excerpt_length, batch_size):

        super().__init__()

        self.batch_size = batch_size
        self.data = data
        self.excerpt_length = excerpt_length

    def __len__(self):

        return len(self.data) // (self.excerpt_length * self.batch_size)

    def __getitem__(self, index):

        i_start = index * self.excerpt_length * self.batch_size
        i_end = (index + 1) * self.excerpt_length * self.batch_size
        return self.data[i_start:i_end].reshape(self.batch_size, self.excerpt_length)

    def on_epoch_end(self):

        pass





class AutoEncoderGenerator(tf.keras.utils.Sequence):

    def __init__(self, generator):

        super().__init__()

        self.generator = generator

    def __len__(self):

        return len(self.generator)

    def __getitem__(self, batch_index):

        x = self.generator[batch_index]
        return x, x

    def on_epoch_end(self):
        self.generator.on_epoch_end()


