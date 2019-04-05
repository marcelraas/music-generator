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


class SongMatchingSampler(tf.keras.utils.Sequence):

    def __init__(self, wave_data, num_batches_per_epoch, batch_size, excerpt_length):

        super().__init__()

        self.num_batches_per_epoch = num_batches_per_epoch
        self.excerpt_length = excerpt_length
        self.batch_size = batch_size
        self.wave_data = wave_data

        self.wave_data_length = self.wave_data.shape[1]

        self.song_offsets = None
        self.song_ids = None
        self.is_same_song = None

        self.on_epoch_end()

    def __len__(self):

        return self.num_batches_per_epoch

    def __getitem__(self, item):

        # First get full song data
        x_full_song = self.wave_data[self.song_ids[item, :, :]]  # batch_idx, song a/b, sample_idx

        # Now get the excerpt data
        batch_song_offsets = self.song_offsets[item, :, :]  # batch_idx, song a/b
        x_excerpts = np.empty(shape=[self.batch_size, 2, self.excerpt_length])

        for batch_idx, offset in enumerate(batch_song_offsets):
            x_excerpts[batch_idx, 0, :] = x_full_song[batch_idx, 0, offset[0]:offset[0] + self.excerpt_length]
            x_excerpts[batch_idx, 1, :] = x_full_song[batch_idx, 1, offset[1]:offset[1] + self.excerpt_length]

        targets = self.is_same_song[item, :]

        return x_excerpts, targets

    def on_epoch_end(self):

        max_idx = self.wave_data_length - self.excerpt_length

        self.song_offsets = np.random.randint(0, max_idx,
                                              size=[self.num_batches_per_epoch, self.batch_size, 2])

        self.song_ids = np.random.randint(0, len(self.wave_data),
                                          size=[self.num_batches_per_epoch, self.batch_size, 2])

        # Ignoring that occasional same song can be sampled
        self.is_same_song = same_song_ids = np.random.uniform(0, 1, size=[self.num_batches_per_epoch, self.batch_size]) > 0.5
        self.song_ids[:, :, 1] = same_song_ids * self.song_ids[:, :, 0] + (1 - same_song_ids) * self.song_ids[:, :, 1]



