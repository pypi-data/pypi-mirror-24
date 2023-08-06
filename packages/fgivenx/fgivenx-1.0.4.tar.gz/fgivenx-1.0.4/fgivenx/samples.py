import numpy
import tqdm
from fgivenx.parallel import openmp_apply, mpi_apply, rank
from fgivenx.io import CacheError, check_cache


def trim_samples(samples, weights, ntrim=0):
    """ Make samples equally weighted, and trim if desired.

    Parameters
    ----------
    samples: numpy.array
        See argument of fgivenx.compute_contours for more detail.

    weights: numpy.array
        See argument of fgivenx.compute_contours for more detail.

    Keywords
    --------
    ntrim: int
        Number of samples to trim to. If <=0 do nothing.
    """

    n = len(weights)
    weights /= weights.max()
    choices = numpy.random.rand(n) < weights

    new_samples = samples[choices]

    if ntrim > 0:
        new_samples = numpy.random.choice(new_samples)

    return new_samples


def compute_samples(f, x, samples, **kwargs):
    """ Apply f(x,theta) to x array and theta in samples.

    Parameters
    ----------
    See arguments of fgivenx.compute_contours

    Keywords
    --------
    parallel: str
        See arguments of fgivenx.compute_contours

    Returns
    -------
    An array of samples at each x. shape=(len(x),len(samples),)
    """

    parallel = kwargs.pop('parallel', '')
    nprocs = kwargs.pop('nprocs', None)
    comm = kwargs.pop('comm', None)
    cache = kwargs.pop('cache', None)

    if cache is not None:
        try:
            return check_cache(cache.fsamps, x, samples)  
        except CacheError as e:
            print(e.args[0])
            del cache.masses

    if parallel is '':
        fsamps = [f(x, theta) for theta in tqdm.tqdm(samples)]
    elif parallel is 'openmp':
        fsamps = openmp_apply(f, samples, precurry=(x,), nprocs=nprocs)
    elif parallel is 'mpi':
        fsamps = mpi_apply(lambda theta: f(x, theta), samples, comm=comm)
    else:
        raise ValueError("keyword parallel=%s not recognised,"
                         "options are 'openmp' or 'mpi'" % parallel)

    fsamps = numpy.array(fsamps).transpose().copy()

    if cache is not None and rank(comm) is 0:
        cache.fsamps = x, samples, fsamps

    return fsamps


def samples_from_getdist_chains(params,file_root=None,chains_file=None,paramnames_file=None):
    """ Extract samples and weights from getdist chains.

    Parameters
    ----------
    params: list(str)
        Names of parameters to be supplied to second argument of f(x|theta).

    file_root: str
        Root name for getdist chains files. This script requires
        - file_root.txt
        - file_root.paramnames

    Returns
    -------
    samples: numpy.array
        2D Array of samples. samples.shape=(# of samples, len(params),)

    weights: numpy.array
        Array of weights. samples.shape = (len(params),)
    """

    # Get the full data
    if file_root is not None:
        chains_file = file_root + '.txt'
        paramnames_file = file_root + '.paramnames' 

    data = numpy.loadtxt(chains_file '.txt')
    weights = data[:, 0]

    # Get the paramnames
    paramnames = numpy.loadtxt(paramnames_file, dtype=str)
    if len(paramnames.shape) is 2:
        paramnames = paramnames[:, 0]

    # Get the relevant samples
    indices = [2+list(paramnames).index(p) for p in params]
    samples = data[:, indices]

    return samples, weights
