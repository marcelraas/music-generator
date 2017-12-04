import numpy as np


def bounded_random_walk_mirror(steps, start_value, min, max):
    n_vals = len(steps) + 1
    r = np.zeros(n_vals)
    r[0] = start_value
    for i, step in enumerate(steps):
        r[i+1] = r[i] + step
        if r[i+1] >= max:
            r[i+1] = max - 1 - (r[i+1] - max)
        if r[i+1] < min:
            r[i+1] = min - (r[i+1] - min)

    return r
