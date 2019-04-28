
import tensorflow as tf
from tensorflow import keras
from music_generator.basic import signalproc
import numpy as np
from tensorflow.keras.layers import Dense, Lambda, PReLU, Input, Dropout, Activation


class RegenModelGru(object):

    def __init__(self, fft_size, num_timesteps):

        self.fft_size = fft_size
        self.num_timesteps = num_timesteps

    def build_model(self):

        def reshape_input(inp):
            return tf.reshape(inp, [self.fft_size, self.num_timesteps])

        def reshape_to_output(layer):
            return tf.reshape(layer, [self.fft_size * self.num_timesteps])

        def apply_fft(x):
            x_complex = tf.cast(x, dtype=tf.complex64)
            x_fft = tf.fft(x_complex)

            return tf.concat([tf.real(x_fft), tf.imag(x_fft)], axis=1)


        inp = keras.layers.Input([self.fft_size*self.num_timesteps])



        reshaped = keras.layers.Lambda(reshape_input)(inp)



        output = keras.layers.Lambda(reshape_to_output)(reshaped)
        return keras.models.Model(inp, output)


class RegenModelFft(object):

    def __init__(self, batch_size, learning_rate=1e-4):

        self.batch_size = batch_size
        self.learning_rate = learning_rate

    def build_model(self):

        def fft_loss(y_target, y_predicted):
            y_target_complex = tf.cast(y_target, dtype=tf.complex64)
            y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

            loss = tf.square(tf.abs(tf.signal.fft(y_target_complex)) -
                             tf.abs(tf.signal.fft(y_predicted_complex)))
            return loss

        def forward_fft(x):
            x_complex = tf.cast(x, dtype=tf.complex64)
            x_fft = tf.signal.fft(x_complex)

            return tf.concat([tf.math.real(x_fft), tf.math.imag(x_fft)], axis=1)

        def backward_fft(x):
            print(x.shape)

            real, imag = tf.split(x, num_or_size_splits=2, axis=1)
            x_complex = tf.complex(real, imag)

            x_complex = tf.signal.ifft(x_complex)
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

    def __init__(self, batch_size, learning_rate=1e-4, loss_fct='mse'):

        self.batch_size = batch_size
        self.learning_rate = learning_rate

        if loss_fct == 'fft_loss':
            self.loss_fct = self.fft_loss
        else:
            self.loss_fct = loss_fct

    def fft_loss(self, y_target, y_predicted):
        y_target_complex = tf.cast(y_target, dtype=tf.complex64)
        y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

        loss = tf.square(tf.abs(tf.signal.fft(y_target_complex)) -
                         tf.abs(tf.signal.fft(y_predicted_complex)))
        return loss

    def build_model(self):

        def fft_loss(y_target, y_predicted):
            y_target_complex = tf.cast(y_target, dtype=tf.complex64)
            y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

            loss = tf.square(tf.abs(tf.signal.fft(y_target_complex)) -
                             tf.abs(tf.signal.fft(y_predicted_complex)))
            return loss


        def apply_fft(x):
            x_complex = tf.cast(out, dtype=tf.complex64)
            return tf.signal.fft(x_complex)

        def apply_ifft(x):
            return tf.math.real(tf.signal.ifft(x))

        def create_abs_branch(x):

            return tf.abs(x)

        def create_angle_branch(x):

            return tf.math.angle(x)

        def combine_and_inverse_fft(args):
            abs_branch, angle_branch = args

            real = abs_branch * tf.cos(angle_branch)
            imag = abs_branch * tf.sin(angle_branch)

            x_complex = tf.complex(real, imag)
            x_reverse = tf.math.real(tf.signal.ifft(x_complex))
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
        abs_branch = Dropout(0.01)(abs_branch)
        abs_branch = Dense(abs_branch.shape[1].value)(abs_branch)
        abs_branch = PReLU()(abs_branch)

        out = keras.layers.Lambda(combine_and_inverse_fft, output_shape=[self.batch_size])([abs_branch, angle_branch])

        ##
        model = keras.models.Model(inp, out)  # type: keras.models.Model

        model.compile(keras.optimizers.Adam(lr=self.learning_rate), loss=self.loss_fct)
        return model


class FftBranchesFilter(object):

    def __init__(self, batch_size, learning_rate=1e-4, loss_fct='mse'):

        self.batch_size = batch_size
        self.learning_rate = learning_rate

        if loss_fct == 'fft_loss':
            self.loss_fct = self.fft_loss
        else:
            self.loss_fct = loss_fct

    def fft_loss(self, y_target, y_predicted):
        y_target_complex = tf.cast(y_target, dtype=tf.complex64)
        y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

        loss = tf.square(tf.abs(tf.signal.fft(y_target_complex)) -
                         tf.abs(tf.signal.fft(y_predicted_complex)))
        return loss

    def build_model(self):

        def fft_loss(y_target, y_predicted):
            y_target_complex = tf.cast(y_target, dtype=tf.complex64)
            y_predicted_complex = tf.cast(y_predicted, dtype=tf.complex64)

            loss = tf.square(tf.abs(tf.signal.fft(y_target_complex)) -
                             tf.abs(tf.signal.fft(y_predicted_complex)))
            return loss

        def apply_fft(x):
            x_complex = tf.cast(x, dtype=tf.complex64)
            return tf.signal.fft(x_complex)

        def apply_ifft(x):
            return tf.math.real(tf.signal.ifft(x))

        def create_abs_branch(x):

            return tf.abs(x)

        def create_angle_branch(x):

            return tf.math.angle(x)

        def combine_and_inverse_fft(args):
            abs_branch, angle_branch = args

            real = abs_branch * tf.cos(angle_branch)
            imag = abs_branch * tf.sin(angle_branch)

            x_complex = tf.complex(real, imag)
            x_reverse = tf.math.real(tf.signal.ifft(x_complex))
            return x_reverse

        inp = Input(shape=(self.batch_size,))

        out = Lambda(apply_fft, output_shape=[self.batch_size])(inp)

        # FFT branching
        abs_branch = keras.layers.Lambda(create_abs_branch, output_shape=[self.batch_size])(out)
        angle_branch = keras.layers.Lambda(create_angle_branch, output_shape=[self.batch_size])(out)

        # Compute filter
        filter_branch = Lambda(lambda x: x / self.batch_size)(abs_branch)
        filter_branch = Dense(abs_branch.shape[1])(filter_branch)
        filter_branch = PReLU()(filter_branch)
        # filter_branch = Dropout(0.01)(filter_branch)
        filter_branch = Dense(abs_branch.shape[1])(filter_branch)
        filter_branch = Activation('sigmoid')(filter_branch)

        # Apply filter on abs branch
        abs_branch = Lambda(lambda x: x[0] * x[1])([abs_branch, filter_branch])

        out = keras.layers.Lambda(combine_and_inverse_fft, output_shape=[self.batch_size])([abs_branch, angle_branch])

        ##
        model = keras.models.Model(inp, out)  # type: keras.models.Model

        model.compile(keras.optimizers.Adam(lr=self.learning_rate), loss=self.loss_fct)
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