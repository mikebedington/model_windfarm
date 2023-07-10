


all_exp = ['seagrass_false_1.nc', 'seagrass_true_0_5.nc', 'seagrass_true_1.nc', 'seagrass_true_new_profile.nc',
		'seagrass_true_new_profile2.nc', 'seagrass_true_new_profile3.nc', 'seagrass_true_new_profile4.nc']
all_exp = ['base_output.nc', 'test0.nc', 'test1.nc', 'test2.nc', 'test3.nc', 'test4.nc', 'test5.nc']
all_exp = ['base_output.nc', 'test5.nc']

all_ds = [nc.Dataset(this_file) for this_file in all_exp]

all_labels = ['No seagrass', 'Seagrass 0.4m XPrat 0.5', 'Seagrass 0.4m', 'Seagrass 1m', 'Seagrass 4m', 'Seagrass 4m no ext', 'Seagrass 4m no ext and coeff 1']
all_labels = ['No seagrass', 'Test0', 'Test1', 'Test2', 'Test3', 'Test4', 'Test5']
all_labels = ['No seagrass', 'Test5']

plot_vars = ['u', 'v', 'P', 'taux', 'tke', 'xP']
plot_vars = ['u', 'v', 'P', 'taux', 'tke', 'xP', 'temp', 'N1_p', 'N3_n', 'P1_c', 'P2_c', 'P3_c', 'P4_c', 'Z4_c', 'Z5_c', 'Z6_c', 'L2_c']

for var in plot_vars:
	if all_ds[0][var][:].shape[1] == all_ds[0]['z'][:].shape[1]:
		vert_coord = 'z'
	else:
		vert_coord = 'zi'

	plt.figure(figsize=[10,14])
	for this_ds in all_ds:
		plt.plot(np.mean(np.squeeze(this_ds[var][:]), axis=0), np.squeeze(this_ds[vert_coord][0,...]))
	plt.legend(all_labels)
	plt.title(f'{var} - {this_ds[var].long_name}')
	plt.tight_layout()
	plt.savefig(f'gotm_{var}.png', dpi=180)
	plt.close()



input_file = np.loadtxt('seagrass.dat', skiprows=1)

plt.plot(input_file[:,0], np.arange(0,len(input_file)))
plt.plot(input_file[:,1], np.arange(0,len(input_file)))
plt.plot(input_file[:,2], np.arange(0,len(input_file)))

# Write a new seagrass.dat

profile = np.linspace(0.05, 0.91, 87)*4
ext = input_file[:,1]
coeff = input_file[:,2]

def write_seagrass(profile, ext, coeff, outname='seagrass.dat'):
	no_lines = len(profile)
	with open(outname, 'w') as f:
	    f.write(f'{no_lines}\n')

		for i in np.arange(0,no_lines):
			f.write(f'      {profile[i]:.5f}      {ext[i]:.5f}      {coeff[i]:.5f}\n')
        



profile = [0, 30]
ext = np.ones(len(profile))*0.01
coeff = np.ones(len(profile))*0.4
