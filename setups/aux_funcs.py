import numpy as np


def write_seagrass_dat(deps, coeff, ext, x_rate, outfile='seagrass.dat', reinterp=None):
	if reinterp is not None:
		coeff = np.interp(deps, reinterp, coeff)
		ext = np.interp(deps, reinterp, ext)
		x_rate = np.interp(deps, reinterp, x_rate)

	n_deps = len(deps)

	with open(outfile, 'w') as f:
		f.write(f'{n_deps} \n')
		for i in np.arange(0,n_deps):
			f.write(f'{deps[i]:0.6f}     {coeff[i]:0.6f}      {ext[i]:0.6f}      {x_rate[i]:0.6f}\n')

