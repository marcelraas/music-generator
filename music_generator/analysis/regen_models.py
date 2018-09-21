
import tensorflow as tf
import keras
from music_generator.basic import signalproc
import numpy as np
from keras.layers import Dense, Lambda, PReLU, Input


class RegenModelFft(object):

    def __init__(self, batch_size, learning_rate=1e-4):

        self.batch_size = batch_size
        self.learning_rate = learning_rate

    def build_model(self):

        def fft_loss(y_target, y_predicted):
            y_target_complex = tf.cast(y_target, dtype=tf.complex64)
            y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

            loss = tf.square(tf.abs(tf.fft(y_target_complex)) -
                             tf.abs(tf.fft(y_predicted_complex)))
            return loss

        def forward_fft(x):
            x_complex = tf.cast(x, dtype=tf.complex64)
            x_fft = tf.fft(x_complex)

            return tf.concat([tf.real(x_fft), tf.imag(x_fft)], axis=1)

        def backward_fft(x):
            print(x.shape)

            real, imag = tf.split(x, num_or_size_splits=2, axis=1)
            x_complex = tf.complex(real, imag)

            x_complex = tf.ifft(x_complex)
            x_real = tf.cast(tf.abs(x_complex), dtype=tf.float32)
            return x_real

        inp = keras.models.Input(shape=(self.batch_size,))
        out = inp

        out = keras.layers.Lambda(forward_fft, output_shape=(self.batch_size * 2,))(out)
        out = keras.layers.Dense(self.batch_size // 2)(out)
        # ffw = keras.layers.PReLU()(ffw)
        out = keras.layers.Dense(self.batch_size * 2)(out)
        out = keras.layers.Lambda(backward_fft, output_shape=(self.batch_size,))(out)

        model = keras.models.Model(inp, out)  # type: keras.models.Model

        model.compile(keras.optimizers.Adam(lr=self.learning_rate), loss=fft_loss)
        return model


class FftBranches(object):

    def __init__(self, batch_size, learning_rate=1e-4):

        self.batch_size = batch_size
        self.learning_rate = learning_rate

    def build_model(self):

        def fft_loss(y_target, y_predicted):
            y_target_complex = tf.cast(y_target, dtype=tf.complex64)
            y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

            loss = tf.square(tf.abs(tf.fft(y_target_complex)) -
                             tf.abs(tf.fft(y_predicted_complex)))
            return loss


        def apply_fft(x):
            x_complex = tf.cast(out, dtype=tf.complex64)
            return tf.fft(x_complex)

        def apply_ifft(x):
            return tf.real(tf.ifft(x))

        def create_abs_branch(x):

            return tf.abs(x)

        def create_angle_branch(x):

            return tf.angle(x)

        def combine_and_inverse_fft(args):
            abs_branch, angle_branch = args

            real = abs_branch * tf.cos(angle_branch)
            imag = abs_branch * tf.sin(angle_branch)

            x_complex = tf.complex(real, imag)
            x_reverse = tf.real(tf.ifft(x_complex))
            return x_reverse

        n_nodes = self.batch_size

        inp = Input(shape=(self.batch_size,))
        out = inp

        out = Lambda(apply_fft, output_shape=[self.batch_size])(out)

        # out = keras.layers.Lambda(apply_ifft, output_shape=[self.batch_size])(out)

        # FFT branching
        abs_branch = keras.layers.Lambda(create_abs_branch, output_shape=[self.batch_size])(out)
        angle_branch = keras.layers.Lambda(create_angle_branch, output_shape=[self.batch_size])(out)

        # Apply network logic on abs branch
        abs_branch = Dense(abs_branch.shape[1].value)(abs_branch)
        abs_branch = PReLU()(abs_branch)
        abs_branch = Dense(abs_branch.shape[1].value)(abs_branch)
        abs_branch = PReLU()(abs_branch)

        out = keras.layers.Lambda(combine_and_inverse_fft, output_shape=[self.batch_size])([abs_branch, angle_branch])

        ##
        model = keras.models.Model(inp, out)  # type: keras.models.Model

        model.compile(keras.optimizers.Adam(lr=self.learning_rate), 'mse') # , loss=fft_loss)
        return model


class RegenModel(object):

    def __init__(self, model, fragment_length):

        self.model = model
        self.fragment_length = fragment_length

    @staticmethod
    def x_fade_profile(batch_dim):
        x = np.arange(batch_dim)
        return 1 - abs(x - (batch_dim / 2)) / (batch_dim / 2)

    def predict(self, input_track):

        dim = self.fragment_length
        n_batches = int(len(input_track) / dim) - 1
        pred_batches = input_track[0:n_batches * dim].reshape((-1, dim))

        pred_batches_shifted = input_track[dim // 2:n_batches * dim + dim // 2].reshape((-1, dim))

        xfp = self.x_fade_profile(dim)

        x0 = np.array([xfp * batch for batch in self.model.predict(pred_batches)]).reshape(-1)
        x1 = np.array([xfp * batch for batch in self.model.predict(pred_batches_shifted)]).reshape(-1)

        return signalproc.mix_at(x0, x1, dim // 2)