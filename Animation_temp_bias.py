import matplotlib.pyplot as plt; import numpy as np; from netCDF4 import Dataset; from datetime import datetime, timedelta; from mpl_toolkits.basemap import Basemap
import matplotlib as mpl; import os, sys; import calendar;  from ezhen.plotbcz import *;  from Get_grid import *

lo = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)
folder = os.path.abspath("/home/eivanov/coawst_data_prrocessing/Temporal/Former/Animation/Temperature")
cmap=mpl.cm.bwr
mintemp=-4; maxtemp=4; division=0.25
clevs = np.arange(mintemp,maxtemp,division)
name='/media/sf_Swap-between-windows-linux/DATA_INPUT_ROMS/Mercator/IFREMER-NWS-SST-L4-REP-OBS_FULL_TIME_SERIE_1520866230672.nc'
xyc='axes points'

ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Former/OW_sstODYSSEA_PARENT.nc', 'r', format='NETCDF4')
ncdata2 = Dataset(name, 'r', format='NETCDF4')
t=ncdata1.variables['time'][:]
sp=np.shape(ncdata1.variables['sst'][0])

odys = Get_grid_ODYSSEA_Nest(name)
odys.mask_t[-1,:]=0
lons_p, lats_p = odys.lon_t, odys.lat_t


def PRINT_PNG(w,time):
	#tempo = m1.transform_scalar(w,lons_p[0],lats_p[:,0],nx,ny)
	#CS3 = m1.imshow(tempo,cmap,vmin=mintemp,vmax=maxtemp)
	CS3 = m1.contourf(x1,y1,w,clevs,cmap=cmap)
	ann = ax.annotate('%s' %(calendar.month_name[time+1]), xy=(0,0),  xycoords=xyc,xytext=(325,20), textcoords=xyc,fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	file_name = os.path.abspath(folder + "/temp%s" %(time+1)+".png"); print calendar.month_name[time+1]; fig.savefig(file_name, dpi=200); ann.remove()#; CS3.remove();


fig, ax, cax, m1 = grid_instance(llcrnrlon=0, urcrnrlon=4, llcrnrlat=50, urcrnrlat=53, lat_ts=51.5, r='i', discr=0.5, caxx='vertical')		# build the grid
xz,yz = bcz_bound()
x, y = m1(xz, yz)
m1.plot(x,y,color='black',linewidth=1.0)
x1, y1 = m1(lons_p, lats_p)
nx = int((m1.xmax-m1.xmin)/2670.); ny = int((m1.ymax-m1.ymin)/3250.)

norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp)
bounds=np.arange(mintemp,maxtemp+division,division)
mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')

roms=np.zeros((12,sp[0],sp[1]))
od=np.zeros((12,sp[0],sp[1]))
day=np.zeros((12))

for i in range(len(t)):
	roms[lo(int(t[i])).month-1] = roms[lo(int(t[i])).month-1]+ncdata1.variables['sst'][i,:,:]
	od[lo(int(t[i])).month-1] = od[lo(int(t[i])).month-1]+ncdata2.variables['analysed_sst'][i,:,:]-273.15
	day[lo(int(t[i])).month-1] = day[lo(int(t[i])).month-1]+1

for n in range(12):
	ww = (roms[n]-od[n])/day[n]
	w = np.ma.masked_where(abs(odys.mask_t-1),ww)
	PRINT_PNG(w,n)

