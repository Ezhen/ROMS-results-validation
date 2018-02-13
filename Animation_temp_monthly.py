import matplotlib.pyplot as plt; import numpy as np; from netCDF4 import Dataset; from datetime import datetime, timedelta; from mpl_toolkits.basemap import Basemap
import matplotlib as mpl; import os, sys; import calendar;  from ezhen.plotbcz import *

lo = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)
folder = os.path.abspath("Animation/Temperature")
cmap=mpl.cm.jet
mintemp=4; maxtemp=20; division=1
clevs = np.arange(mintemp,maxtemp,division)
xyc='axes points'

ncdata1 = Dataset('Replotting/OW_bulk.nc', 'r', format='NETCDF4')
ncdata2 = Dataset('Replotting/OWc_bulk.nc', 'r', format='NETCDF4')
t=ncdata1.variables['time'][:]
sp_p=np.shape(ncdata1.variables['sst'][0])
sp_c=np.shape(ncdata2.variables['sst'][0])

mask_p=ncdata1.variables['mask_rho'][:]; mask_c=ncdata2.variables['mask_rho'][:]
lons_p, lats_p = ncdata1.variables['lon_rho'][:], ncdata1.variables['lat_rho'][:]
lons_c, lats_c = ncdata2.variables['lon_rho'][:], ncdata2.variables['lat_rho'][:]


def PRINT_PNG(w_p,w_c,time):
	CS1 = m1.contourf(x1,y1,w_p,clevs,cmap=cmap)
	CS2 = m1.contourf(x2,y2,w_c,clevs,cmap=cmap)
	ann = ax.annotate('%s' %(calendar.month_name[time+1]), xy=(0,0),  xycoords=xyc,xytext=(275,20), textcoords=xyc,fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	file_name = os.path.abspath(folder + "/temp%s" %(time+1)+".png"); print calendar.month_name[time+1]; fig.savefig(file_name, dpi=200); ann.remove()#; CS1.remove(); CS2.remove();


#fig, ax, cax, m1 = grid_instance(llcrnrlon=0, urcrnrlon=4, llcrnrlat=50, urcrnrlat=53, lat_ts=51.5, r='i', discr=0.5, caxx='vertical')		# build the grid
fig, ax, cax, m1 = grid_instance(llcrnrlon=-3, urcrnrlon=6.0, llcrnrlat=49, urcrnrlat=55.0, lat_ts=51.5, r='i', discr=0.5, caxx='vertical')
xz,yz = bcz_bound()
x, y = m1(xz, yz)
m1.plot(x,y,color='black',linewidth=1.0)
x1, y1 = m1(lons_p, lats_p)
x2, y2 = m1(lons_c, lats_c)
m1.plot(x1[0],y1[0],color='k',linewidth=1); m1.plot(x1[-1],y1[-1],color='k',linewidth=1); m1.plot(x1[:,0],y1[:,0],color='k',linewidth=1); m1.plot(x1[:,-1],y1[:,-1],color='k',linewidth=1)
m1.plot(x2[0],y2[0],color='k',linewidth=1); m1.plot(x2[-1],y2[-1],color='k',linewidth=1); m1.plot(x2[:,0],y2[:,0],color='k',linewidth=1); m1.plot(x2[:,-1],y2[:,-1],color='k',linewidth=1)

norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp)
bounds=np.arange(mintemp,maxtemp+division,division)
mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')

roms_p=np.zeros((12,sp_p[0],sp_p[1]))
roms_c=np.zeros((12,sp_c[0],sp_c[1]))
day=np.zeros((12))

for i in range(len(t)):
	roms_p[lo(int(t[i])).month-1] = roms_p[lo(int(t[i])).month-1]+ncdata1.variables['sst'][i,:,:]
	roms_c[lo(int(t[i])).month-1] = roms_c[lo(int(t[i])).month-1]+ncdata2.variables['sst'][i,:,:]
	day[lo(int(t[i])).month-1] = day[lo(int(t[i])).month-1]+1

for n in range(12):
	ww_p = roms_p[n]/day[n]
	ww_c = roms_c[n]/day[n]
	w_p = np.ma.masked_where(abs(mask_p-1),ww_p)
	w_c = np.ma.masked_where(abs(mask_c-1),ww_c)
	PRINT_PNG(w_p,w_c,n)

