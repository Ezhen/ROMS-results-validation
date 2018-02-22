#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import numpy
import matplotlib.pyplot as plt
import datetime
from netCDF4 import Dataset
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
#import sys
#sys.path.insert(0, '../cmocean')
import cmocean.cm as cm

cmap=cm.amp


def get_ellipse_coords(a=0.0, b=0.0, x=0.0, y=0.0, angle=0.0, k=2):
    """ Draws an ellipse using (360*k + 1) discrete points; based on pseudo code
    given at http://en.wikipedia.org/wiki/Ellipse
    k = 1 means 361 points (degree by degree)
    a = major axis distance,
    b = minor axis distance,
    x = offset along the x-axis
    y = offset along the y-axis
    angle = clockwise rotation [in degrees] of the ellipse;
        * angle=0  : the ellipse is aligned with the positive x-axis
        * angle=30 : rotated 30 degrees clockwise from positive x-axis
    """
    pts = np.zeros((360*k+1, 2))

    beta = -angle * np.pi/180.0
    sin_beta = np.sin(beta)
    cos_beta = np.cos(beta)
    alpha = np.radians(np.r_[0.:360.:1j*(360*k+1)])
 
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    
    pts[:, 0] = x + (a * cos_alpha * cos_beta - b * sin_alpha * sin_beta)
    pts[:, 1] = y + (a * cos_alpha * sin_beta + b * sin_alpha * cos_beta)

    return pts



def ellipse_calc(Au,Av,PHIu,PHIv):
	"""
	 The function calculates ellipse parameters out of two  
         velocity components and the corresponding phases       
	 							   
	 		Attributes				   
	 * Au - eastward velocity component			   
	 * Av - northward velocity component			   
	 * PHIu - phase of eastward velocity			   
	 * PHIv - phase of northward velocity	 	   
	"""
	# Assume the input phase lags are in degrees and convert them in radians.
	PHIu = PHIu/180*np.pi
	PHIv = PHIv/180*np.pi
	# Make complex amplitudes for u and v
	u = 1.0001*Au*np.exp(-1j*PHIu)
	v = 1.0001*Av*np.exp(-1j*PHIv)
	# Calculate complex radius of anticlockwise and clockwise circles:
	wp = (u+1j*v)/2     	 #for anticlockwise circles
	wm = np.conj(u-1j*v)/2	 #for clockwise circles
	# and their amplitudes and angles
	Wp = np.abs(wp)
	Wm = np.abs(wm)
	THETAp = np.angle(wp)
	THETAm = np.angle(wm)
	# calculate ep-parameters (ellipse parameters)
	SEMA = Wp+Wm              # Semi  Major Axis, or maximum speed
	SEMI = Wp-Wm              # Semin Minor Axis, or minimum speed
	ECC = SEMI*1.0001/SEMA          # Eccentricity

	PHA = (THETAm-THETAp)/2   # Phase angle, the time (in angle) when 
		                       # the velocity reaches the maximum
	INC = (THETAm+THETAp)/2   # Inclination, the angle between the 
		                       # semi major axis and x-axis (or u-axis).
	# convert to degrees for output
	PHA = PHA/np.pi*180         
	INC = INC/np.pi*180         
	THETAp = THETAp/np.pi*180
	THETAm = THETAm/np.pi*180

	return SEMA,SEMI,INC


def PRINT_PNG(w,grid):
	"""
	 The function plots velocity as a contour field and a quiver (vectors) 
	 									   
	 		Attributes						   
	 * u - eastward velocity component					   
	 * v - northward velocity component					   
	 * w - magnitude of the total velocity vector			   
	 * time - time moment in seconds (ocean_time in ROMS)		   
	 * grid - name of the grid to save an image				   
	"""
	m1.contourf(x1,y1,w,clevs,cmap=cmap)
	#kk = m1.quiver(x1[::prec,::prec],y1[::prec,::prec],u[::prec,::prec],v[::prec,::prec],color='black',scale=20,linewidth=w[::prec,::prec].flatten(),angles='xy',edgecolor='None') # color='#A52A2A'
	#ann = ax.annotate('%s' %(d2(time).strftime("%d %B %Y %H:00")), xy=(0,0),  xycoords='axes points',xytext=(175,20), textcoords='axes points',fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))

def BUILD_GRID(llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts,discr,lons_p,lats_p):
	"""
	 This function makes a grid frame with Basemap     
	 						       
	 		Attributes 			       
	 * llcrnrlon - longitude of the lower left corner  
	 * urcrnrlon - longitude of the upper right corner 
	 * llcrnrlat - latitude of the lower left corner   
	 * urcrnrlat - latitude of the upper right corner  
	 * lat_ts    - central latitude                    
	 * discr     - discretization of the grid          
	 * lons_p    - mesh of longitudes taken from ROMS  
	 * lats_p    - mesh of latitudes taken from ROMS   
	"""
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
	"""
	 This function makes a colorbar for data on a map 
	"""
	division = (var_max-var_min) / 50.
	norm = mpl.colors.Normalize(vmin=var_min, vmax=var_max)
	bounds=np.arange(var_min,var_max+division,division)
	cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')
	cb.ax.set_title('      Amp [m]',fontsize=12)
	return np.arange(var_min,var_max,division)


if __name__ == '__main__':

	"""
	 Choose which ROMS (or the reference TPXO) grid you would like to work with and comment all others
	"""

	#path1 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/OW_zeta.nc'; path2 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/OW_uv.nc'; grid = 'OW'; each = 1
	#path1 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/TW_zeta.nc'; path2 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/TW_uv.nc'; grid = 'TW'; each = 1
	#path1 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/OWc_zeta.nc'; path2 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/OWc_uv.nc'; grid = 'OWc'; each = 5
	#path1 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/TWc_zeta.nc'; path2 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/TWc_uv.nc'; grid = 'TWc'; each = 5
	path1 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/Tides_parent.nc'; path2 = '/home/eivanov/coawst_data_prrocessing/Temporal/Tide_files/Tides_parent.nc'; grid = 'TPXO'; each = 1

	# Open the file #
	n1 = Dataset(path1, 'r', format='NETCDF4')
	n2 = Dataset(path2, 'r', format='NETCDF4')
	if grid != 'TPXO':
		lons_p, lats_p = n1.variables['lon'][:],n1.variables['lat'][:]
	else:
		lons_p, lats_p = n1.variables['lon_rho'][:],n1.variables['lat_rho'][:]		
	
	# Call the function that builds the grid (llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts,discr,lons_p,lats_p) #
	llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts = 2.1,3.4,51,51.9,51.5
	fig,m1,ax,cax,x1,y1 = BUILD_GRID(llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts,0.25,lons_p,lats_p)
	#fig,m1,ax,cax,x1,y1 = BUILD_GRID(-2,6,49,55,52,0.5,lons_p,lats_p)

	# Choose the colorbar to work with (colorbar minimum, colorbar maximum) #
	var_min,var_max = 0.5,3.0 	# minimum and maximum variable magnitude
	clevs = COLORBAR(var_min,var_max)
	
	if grid != 'TPXO':
		w = n1.variables['M2'][:]
		u = n2.variables['M2_u'][:]
		v = n2.variables['M2_v'][:]
		up = n2.variables['MP2_u'][:]
		vp = n2.variables['MP2_v'][:]
		SEMA,SEMI,INC = ellipse_calc(u,v,up,vp)
	else:
		w = n1.variables['tide_Eamp'][0]
		SEMA = n1.variables['tide_Cmax'][0]
		SEMI = n1.variables['tide_Cmin'][0]
		INC = n1.variables['tide_Cangle'][0]

	# plot data on the map #
	PRINT_PNG(w,grid)
	for i in range(2,len(w),each):
		for j in range(2,len(w.T),each):
			if type(SEMA[i,j]) != numpy.ma.core.MaskedConstant and lons_p[i,j]>llcrnrlon and lons_p[i,j]<urcrnrlon and lats_p[i,j]>llcrnrlat and lats_p[i,j]<urcrnrlat:
				poly = get_ellipse_coords(a=(SEMA[i,j]/25.), b=(SEMI[i,j]/25.), x=lons_p[i,j], y=lats_p[i,j], angle=-INC[i,j], k=2)
				xx,yy = m1(poly[:,0],poly[:,1])
				m1.plot(xx,yy,color='black',linewidth=2.0)

	fig.savefig("%s.png" %(grid), dpi=200)


