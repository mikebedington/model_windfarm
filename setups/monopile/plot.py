o1 = nc.Dataset('mon1.nc')
o2 = nc.Dataset('mon2.nc')

poc1 = o1['R1_c'][:] + o1['R2_c'] + o1['R3_c'] + o1['R4_c'] + o1['R6_c'] + o1['R8_c']
poc2 = o2['R1_c'][:] + o2['R2_c'] + o2['R3_c'] + o2['R4_c'] + o2['R6_c'] + o2['R8_c']

y1 = np.squeeze(o1['Ys_c'][1:,1:,...]).T


time = np.asarray([dt.datetime(2011,1,1) + dt.timedelta(seconds=int(s)) for s in o1['time'][:]])
choose_time = time > dt.datetime(2015,1,1)

poc1 = poc1[choose_time,...]
poc2 = poc2[choose_time,...]

deps = np.cumsum(o1['h'][0,:,0,0])
deps = deps - np.max(deps)

y1 = o1['Ys_c'][choose_time,...]
y2 = o2['Ys_c'][choose_time,...]

poc1 = np.squeeze(poc1[1:,1:,...]).T
poc2 = np.squeeze(poc2[1:,1:,...]).T

y1 = np.squeeze(y1[1:,1:,...]).T
y2 = np.squeeze(y2[1:,1:,...]).T
diff = y1 - y2

diff2 = poc1 - poc2


fig, ax = plt.subplots(2,3,figsize=[15,12])

# Top row - grams of colonising carbon per m2
im1 = ax[0,0].pcolormesh(time[choose_time], deps, y2)
cb1 = plt.colorbar(im1, ax=ax[0,0])
cb1.set_label('g C/m²')

im2 = ax[0,1].pcolormesh(time[choose_time], deps, y1)
cb2 = plt.colorbar(im2, ax=ax[0,1])
cb2.set_label('g C/m²')

im3 = ax[0,2].pcolormesh(time[choose_time], deps, diff, cmap='bwr')
cb3 = plt.colorbar(im3, ax=ax[0,2])
cb3.set_label('g C/m²')

# Add title to top row
fig.text(0.5, 0.92, 'Structure fauna growth', ha='center', fontsize=14, fontweight='bold')


# Bottom row - g/m3 of POC
im4 = ax[1,0].pcolormesh(time[choose_time], deps, poc2)
cb4 = plt.colorbar(im4, ax=ax[1,0])
cb4.set_label('g/m³ POC')

im5 = ax[1,1].pcolormesh(time[choose_time], deps, poc1)
cb5 = plt.colorbar(im5, ax=ax[1,1])
cb5.set_label('g/m³ POC')

im6 = ax[1,2].pcolormesh(time[choose_time], deps, diff2, cmap='bwr')
cb6 = plt.colorbar(im6, ax=ax[1,2])
cb6.set_label('g/m³ POC')

# Add title to bottom row
fig.text(0.5, 0.47, 'POC in water column', ha='center', fontsize=14, fontweight='bold')

# Add title to bottom row
fig.text(0.2, 0.02, 'Original structure', ha='center', fontsize=14)
fig.text(0.48, 0.02, 'Added substrate', ha='center', fontsize=14)
fig.text(0.78, 0.02, 'Difference', ha='center', fontsize=14)


# Set y-axis limits
for a in ax:
    for b in a:
        b.set_ylim([-70,0])

# Clean up date ticks to avoid overlap
for a in ax:
    for b in a:
        b.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=4))
        b.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
        plt.setp(b.xaxis.get_majorticklabels(), rotation=45, ha='right')

fig.savefig('struct_c_change.png')
plt.close()
