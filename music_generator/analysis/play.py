import numpy as np

from simpleaudio import play_buffer


def play_mono_as_stereo(array: np.array,
                        sample_rate=44100,
                        norm=1.0):
    """Plays mono numpy array and waits until done

    The stereo-effect is created by inverting the channels.

    Args:
        array (np.array): numpy array
        sample_rate (int): sample rate
        norm (float): norm

    Returns:
        None
    """

    scale = 2**15 - 1
    array = ((array / norm).clip(-1, 1) * scale).astype(np.int16)

    stereo = np.array([array, -array]).T.flatten()

    po = play_buffer(stereo, 2, 2, sample_rate)
    po.wait_done()


def play_array(array: np.array,
               sample_rate=44100,
               norm=1.0):
    """Plays mono numpy array and waits until done

    Args:
        array (np.array): numpy array
        sample_rate (int): sample rate
        norm (float): norm

    Returns:
        None
    """

    scale = 2**15 - 1
    array = ((array / norm).clip(-1, 1) * scale).astype(np.int16)

    po = play_buffer(array, 1, 2, sample_rate)
    po.wait_done()
