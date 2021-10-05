import os.path
import argparse
import pickle

from matplotlib import pyplot
import numpy
import netCDF4

parser = argparse.ArgumentParser()
parser.add_argument('pickle')
parser.add_argument('output_file')
parser.add_argument('variable')
parser.add_argument('--depth', type=float)
parser.add_argument('--output')
args = parser.parse_args()

if args.output is None:
    args.output = 'observability_%s%s.png' % (args.variable, '' if args.depth is None else '_%sm' % args.depth)

with open(args.pickle, 'rb') as f:
    job_info = pickle.load(f)
simulationdirs = job_info['simulationdirs']
X = job_info['X']
X_zscore = (X - X.mean(axis=0)) / X.std(axis=0)

print('Reading results from ensemble with %i members:' % (len(simulationdirs),))
with netCDF4.Dataset(os.path.join(simulationdirs[0], args.output_file)) as nc:
    z = nc.variables['z'][0, :, 0, 0]   # assume depth does not depend on time or ensemble member
    nctime = nc.variables['time']
    time = netCDF4.num2date(nctime[:], units=nctime.units, only_use_cftime_datetimes=False)
    ncvar = nc.variables[args.variable]
    long_name, units = ncvar.long_name, ncvar.units
    if ncvar.ndim == 4 and args.depth is not None:
        k = numpy.abs(z + args.depth).argmin()
        slc = (slice(None), k, 0, 0)
        shape = (ncvar.shape[0],)
    else:
        slc = (Ellipsis, 0, 0)
        shape = ncvar.shape[:-2]
    Y = numpy.empty((len(simulationdirs),) + shape, dtype=ncvar.dtype)
    for imember, simdir in enumerate(simulationdirs):
        with netCDF4.Dataset(os.path.join(simdir, args.output_file)) as ncmem:
            Y[imember, ...] = ncmem.variables[args.variable][slc]

fig, ax = pyplot.subplots(figsize=(8, 5))
if Y.ndim == 2:
    perc = numpy.percentile(Y, (25, 50, 75), axis=0)
    ax.fill_between(time, Y.min(axis=0), Y.max(axis=0), color='C0', alpha=.5)
    ax.fill_between(time, perc[0, :], perc[-1, :], color='C0')
    ax.plot(time, perc[1, :], '-k')
    ax.set_ylabel('%s (%s)' % (long_name, units))
    ax.grid()
else:
    Y_zscore = (Y - Y.mean(axis=0)) / Y.std(axis=0)
    s = (Y_zscore / X_zscore[..., numpy.newaxis]).mean(axis=0)
    s = Y.std(axis=0) / Y.mean(axis=0)
    c = ax.contourf(time, z, s.T)
    fig.colorbar(c)
fig.savefig(args.output, dpi=150)

