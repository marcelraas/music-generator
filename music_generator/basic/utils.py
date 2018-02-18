import numpy as np
import multiprocessing
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


def elastic_bounded_random_walk(steps, start_value, min, max):
    n_vals = len(steps) + 1
    r = np.zeros(n_vals)
    r[0] = start_value
    for i, step in enumerate(steps):
        r[i+1] = r[i] + step
        if r[i+1] >= max:
            r[i+1] = max - 3
        if r[i+1] < min:
            r[i+1] = min + 3

    return r


def parallel_apply_along_axis(func1d, axis, arr, *args, **kwargs):
    """
    Like numpy.apply_along_axis(), but takes advantage of multiple
    cores.
    """
    # Effective axis where apply_along_axis() will be applied by each
    # worker (any non-zero axis number would work, so as to allow the use
    # of `np.array_split()`, which is only done on axis 0):
    # effective_axis = 1 if axis == 0 else axis
    # if effective_axis != axis:
    #     arr = arr.swapaxes(axis, effective_axis)
    if axis != 0:
        raise ValueError("Only axis = 0 is allowed")
    effective_axis = axis

    # Chunks for the mapping (only a few chunks):
    chunks = [(func1d, effective_axis, sub_arr, args, kwargs)
              for sub_arr in np.array_split(arr, multiprocessing.cpu_count())]

    pool = multiprocessing.Pool()
    individual_results = pool.map(unpacking_apply_along_axis, chunks)
    # Freeing the workers:
    pool.close()
    pool.join()

    out = np.concatenate(individual_results)
    # if effective_axis != axis:
    #     out.swapaxes(axis, effective_axis)
    return out


def unpacking_apply_along_axis(args_as_tuple):
    """
    Like numpy.apply_along_axis(), but and with arguments in a tuple
    instead.

    This function is useful with multiprocessing.Pool().map(): (1)
    map() only handles functions that take a single argument, and (2)
    this function can generally be imported from a module, as required
    by map().
    """
    func1d, axis, arr, args, kwargs = args_as_tuple

    return np.apply_along_axis(func1d, axis, arr, *args, **kwargs)