import numpy as np


def get_max_duration(note_list):
    durations = [n.get_moment_release() for n in note_list]
    return np.max(durations)