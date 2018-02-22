#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import datetime 
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import calendar
#import sys
#sys.path.insert(0, '../cmocean')
import cmocean.cm as cm

lo = lambda x: datetime.datetime(2006,1,1,0,0,0) + datetime.timedelta(seconds=x)
cmap=cmocean.cm.delta


def PRINT_PNG(u,v,w,time,grid,prec):
	""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	"""" The function plots velocity as a contour field and a quiver (vectors) """
	"""" 									   """
	"""" 		Attributes						   """
	"""" * u - eastward velocity component					   """
	"""" * v - northward velocity component					   """
	"""" * w - magnitude of the total velocity vector			   """
	"""" * time - time moment in seconds (ocean_time in ROMS)		   """
	"""" * grid - name of the grid to save an image				   """
	""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	m1.contourf(x1,y1,w,clevs,cmap=cmap)
	kk = m1.quiver(x1[::prec,::prec],y1[::prec,::prec],u[::prec,::prec],v[::prec,::prec],color='black',scale=20,linewidth=w[::prec,::prec].flatten(),angles='xy',edgecolor='None') # color='#A52A2A'
	ann = ax.annotate('%s' %(calendar.month_name[time+1]), xy=(0,0),  xycoords='axes points',xytext=(175,20), textcoords='axes points',fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	file_name = str(d2(time).strftime("%d_%B_%Y_%H")) +"_%s.png" %(grid);  fig.savefig("Residuals/%s" %(file_name), dpi=200); ann.remove(); kk.remove()


def BUILD_GRID(llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts,discr,lons_p,lats_p):
	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	"""" This function makes a grid frame with Basemap     """"
	"""" 						       """"
	"""" 		Attributes 			       """"
	"""" * llcrnrlon - longitude of the lower left corner  """"
	"""" * urcrnrlon - longitude of the upper right corner """"
	"""" * llcrnrlat - latitude of the lower left corner   """"
	"""" * urcrnrlat - latitude of the upper right corner  """"
	"""" * lat_ts    - central latitude                    """"
	"""" * discr     - discretization of the grid          """"
	"""" * lons_p    - mesh of longitudes taken from ROMS  """"
	"""" * lats_p    - mesh of latitudes taken from ROMS   """"
	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
	m1 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='h', ax=ax)
	m1.drawparallels(np.arange(llcrnrlat,urcrnrlat,discr),labels=[1,0,0,1],fontsize=10)
	m1.drawmeridians(np.arange(llcrnrlon,urcrnrlon,discr),labels=[1,1,1,0],fontsize=10)
	m1.drawcoastlines()
	m1.drawmapboundary(fill_color='aqua')
	m1.drawcountries()
	m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	cax = make_axes_locatable(ax).append_axes("right", size=0.4, pad=0.15)
	yz=np.array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361])
	xz=np.array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
	x, y = m1(xz, yz)
	m1.plot(x,y,color='black',linewidth=1.0)
	x1, y1 = m1(lons_p, lats_p)
	return fig,m1,ax,cax,x1,y1


def COLORBAR(var_min,var_max):
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	"""" This function makes a grid frame with Basemap """
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	division = (var_max-var_min) / 50.
	norm = mpl.colors.Normalize(vmin=var_min, vmax=var_max)
	bounds=np.arange(var_min,var_max+division,division)
	cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')
	cb.ax.set_title('ms-1',fontsize=12)
	return np.arange(var_min,var_max,division)



folder = os.path.abspath("Animation/Currents/Month")


# Choose the colorbar to work with (colorbar minimum, colorbar maximum) #
var_min,var_max = -1.5,1.5 	# minimum and maximum variable magnitude
clevs = COLORBAR(var_min,var_max)


#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSSNNAVG_20062008.nc'; grid = 'NN'; prec = 1
path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_AVG_20062008_parent.nc'; grid = 'OW'; prec = 1
#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_AVG_20062008_parent.nc'; grid = 'TW'; prec = 1
#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_AVG_20062008_child.nc'; grid = 'OWc'; prec = 3
#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_AVG_20062008_child.nc'; grid = 'TWc'; prec = 3


n1 = Dataset(path, 'r', format='NETCDF4')
lons_p, lats_p = n1.variables['lon_rho'][:],n1.variables['lat_rho'][:]
sp = np.shape(lons_p)

# Call the function that builds the grid (llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts,discr,lons_p,lats_p) #
#fig,m1,ax,cax,x1,y1 = BUILD_GRID(2.1,3.4,51,51.9,51.5,0.25,lons_p,lats_p)
fig,m1,ax,cax,x1,y1  = BUILD_GRID(2.35,3.25,51.15,51.45,51.5,0.25,lons_p,lats_p)

# Choose the colorbar to work with (colorbar minimum, colorbar maximum) #
var_min,var_max = -1.5,1.5 	# minimum and maximum variable magnitude
clevs = COLORBAR(var_min,var_max)
	
r=np.zeros((12,sp[0],sp[1]))
ru=np.zeros((12,sp[0],sp[1]))
rv=np.zeros((12,sp[0],sp[1]))

day=np.zeros((12))

if PARAM=='AV':
	a,b=0,12
	for i in range(len(t)):
		ru[lo(int(t[i])).month-1] += n1.variables['u_eastward'][i,-1,:,:]
		rv[lo(int(t[i])).month-1] += n1.variables['v_northward'][i,-1,:,:]
		day[lo(int(t[i])).month-1] = day[lo(int(t[i])).month-1]+1
		print i

for n in range(12):
	u = ru[n]/day[n]
	v = rv[n]/day[n]
	w = (u10*u10+v10*v10)**0.5
	PRINT_PNG(u,v,w,n,grid,prec)
