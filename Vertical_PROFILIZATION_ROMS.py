import numpy as np; import matplotlib.pyplot as plt; from netCDF4 import Dataset; from scipy import spatial

# VLIZ stations locations
MP0_lat=51+23/60.+40.04/3600.; MP0_lon=3+2./60.+44.82/3600. # MP0 (Measuring Pile 0, Oostdyckbank)
MP3_lat=51+23/60.+22.57/3600.; MP3_lon=3+11/60.+55.42/3600. # MP3 (Measuring Pile 3, Westhinder)  
MP4_lat=51+25/60.+6.08/3600. ; MP4_lon=3+17/60.+54.88/3600. # MP4 (Measuring Pile 4, Westhinder)

ncdata1 = Dataset('/home/eivanov/COAWST_NEW/his_tds_long_run_10.nc', 'r', format='NETCDF4')
lats = ncdata1.variables['lat_rho'][:]; lons = ncdata1.variables['lon_rho'][:]; hs = ncdata1.variables['h'][:]; width=len(hs.T)

# And the corresponding ROMS locations
aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; 
idxx=spatial.KDTree(aa).query([MP0_lon,MP0_lat])[1]; idxx3=spatial.KDTree(aa).query([MP3_lon,MP3_lat])[1]; idxx4=spatial.KDTree(aa).query([MP4_lon,MP4_lat])[1]
a0=int(idxx/width); b0=int(idxx-(idxx/width)*width); a3=int(idxx3/width); b3=int(idxx3-(idxx3/width)*width); a4=int(idxx4/width); b4=int(idxx4-(idxx4/width)*width)

t = ncdata1.variables['ocean_time'][:]

m1, m2, m3, h1, h2, h3 = np.zeros((15)), np.zeros((15)), np.zeros((15)), 0,0,0
for i in range(len(t)):
	m1 += (ncdata1.variables['u_eastward'][i,:,a0,b0]**2 + ncdata1.variables['v_northward'][i,:,a0,b0]**2)**0.5
	h1 += ncdata1.variables['zeta'][i,a0,b0]
	m2 += (ncdata1.variables['u_eastward'][i,:,a3,b3]**2 + ncdata1.variables['v_northward'][i,:,a3,b3]**2)**0.5
	h2 += ncdata1.variables['zeta'][i,a3,b3]
	m3 += (ncdata1.variables['u_eastward'][i,:,a4,b4]**2 + ncdata1.variables['v_northward'][i,:,a4,b4]**2)**0.5
	h3 += ncdata1.variables['zeta'][i,a4,b4]

cs = ncdata1.variables['Cs_r'][:]
	
h1 = hs[a0,b0] + h1/len(t); m1 = m1/len(t)
h2 = hs[a3,b3] + h2/len(t); m2 = m2/len(t)
h3 = hs[a4,b4] + h3/len(t); m3 = m3/len(t)

fig, ax = plt.subplots(figsize=(12, 8))
plt.plot(m1,h1*cs, label = 'MP0')
plt.plot(m2,h2*cs, label = 'MP3')
plt.plot(m3,h3*cs, label = 'MP4')
plt.xlabel('Speed [m/s]'); plt.ylabel('Depth [m]'); plt.legend(loc=2); fig.savefig('ROMS_vertical_vel.png', dpi=100); plt.show()

