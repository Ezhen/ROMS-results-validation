from netCDF4 import Dataset;import numpy as np; import matplotlib.pyplot as plt; from mpl_toolkits.basemap import Basemap; from mpl_toolkits.axes_grid1 import make_axes_locatable; import matplotlib as mpl
import os; from pylab import *

nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_tides/BOUNDARY_NORTH.nc', 'r', format='NETCDF3')
m2r=nc.variables['MP2'][:]#; s2r=nc.variables['SP2'][:]; n2r=nc.variables['NP2'][:]; 
nc.close()

rr = Dataset('/home/eivanov/coawst_data_prrocessing/Tides_prediction/Tide_local.nc', 'r', format='NETCDF3')
m2t=rr.variables['tide_Ephase'][0,:,:]#; s2t=rr.variables['tide_Ephase'][1,:,:]; n2t=rr.variables['tide_Ephase'][2,:,:]; 
lat=rr.variables['lat_rho'][:]; lon=rr.variables['lon_rho'][:]; maska=rr.variables['mask_rho'][:]; rr.close()

m2=np.zeros((len(m2r),len(m2r.T)))#; s2=np.zeros((len(m2r),len(m2r.T))); n2=np.zeros((len(m2r),len(m2r.T))); 
maska=np.zeros((np.shape(m2r)[0],np.shape(m2r)[1]), dtype=bool)
m2=np.array(np.matrix(m2r)-(np.matrix(m2t)))#; s2=np.array(np.matrix(s2r)-(np.matrix(s2t))); n2=np.array(np.matrix(n2r)-(np.matrix(n2t)));  
maska=np.zeros((np.shape(m2r)[0],np.shape(m2r)[1]), dtype=bool)

maxim=360; division=10
m2[m2>maxim]=maxim#; s2[s2>maxim]=maxim; n2[n2>maxim]=maxim #### Decrease amplitude ratio down to 5

m2=np.ma.array(m2,mask=maska)#; s2=np.ma.array(s2,mask=maska); n2=np.ma.array(n2,mask=maska)

#tide=[m2,s2,n2]; varlist=['MP21','SP21','NP21']; amplitude_roms=[m2r,s2r,n2r]; amplitude_tpox=[m2t,s2t,n2t];
tide=[m2]; varlist=['M21']; amplitude_roms=[m2r]; amplitude_tpox=[m2t]; 
"""
nc = Dataset('Diff.nc', 'w', format='NETCDF3_64BIT')
nc.createDimension('eta', len(lat)); nc.createDimension('xi', len(lat.T))
nc.createVariable('lat', 'f4', ( 'eta', 'xi'))
nc.createVariable('lon', 'f4', ( 'eta', 'xi'))
nc.createVariable('Diff_M2', 'f4', ( 'eta', 'xi'))
nc.createVariable('Diff_S2', 'f4', ( 'eta', 'xi'))
nc.variables['Diff_M2'][:]=tide[0]
nc.variables['Diff_S2'][:]=tide[1]
nc.variables['lat'][:]=lat; nc.variables['lon'][:]=lon
nc.close 
"""
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10)); m1 = Basemap(projection='merc',llcrnrlat=49,urcrnrlat=55,llcrnrlon=-3,urcrnrlon=5,lat_ts=51.5,resolution='h', ax=ax)
y_bcz=np.array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361]); x_bcz=np.array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
m1.drawparallels(np.arange(49,55,0.5),labels=[1,0,0,1],fontsize=10); m1.drawmeridians(np.arange(-3,5,0.5),labels=[1,1,1,0],fontsize=10); m1.drawcoastlines(); m1.drawmapboundary(fill_color='#9999FF')
x4, y4 = m1(x_bcz, y_bcz); cs43 = m1.plot(x4,y4,color='black',linewidth=1.0); x1,y1 = m1(lon,lat); mintemp=-360; maxtemp=maxim+0.1; clevs = np.arange(mintemp,maxtemp,division); bounds=np.arange(mintemp,maxim+division,division)
cax = make_axes_locatable(ax).append_axes("right", size=0.4, pad=0.15); norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp); mpl.colorbar.ColorbarBase(cax, cmap=mpl.cm.gist_ncar, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')
for i in range(0,1):
	CS2 = m1.contourf(x1,y1,tide[i],clevs,cmap=mpl.cm.gist_ncar) 
	#CS2 = m1.contourf(x1,y1,amplitude_roms[i],clevs,cmap=mpl.cm.rainbow)
	#CS2 = m1.contourf(x1,y1,amplitude_tpox[i],clevs,cmap=mpl.cm.rainbow)
	m1.drawcountries(); m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	lol=ax.annotate('%s' %(varlist[i][:-1]), xy=(0,0),  xycoords='axes points',xytext=(300,20), family='Courier New, monospace',textcoords='axes points',fontsize=50, bbox=dict(facecolor='none', edgecolor='none', pad=5.0))
	file_name = os.path.abspath("%s" %(varlist[i])+".png"); fig.savefig(file_name, dpi=200); lol.remove()

