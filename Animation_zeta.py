#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
from ezhen.plotbcz import *
import pyroms
import cmocean.cm as cm

def PRINT_PNG(w1,w2,grid_flag,var,flag,fig,m1,ax,x1,y1,x2,y2,clevs,cmap):
	CS1 = m1.contourf(x1,y1,w1,clevs,cmap=cmap)
	if flag == 'YES':
		CS2 = m1.contourf(x2,y2,w2,clevs,cmap=cmap)
	ann = ax.annotate('M2', xy=(0,0), xycoords='axes points',xytext=(250,20), textcoords='axes points',fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	fig.savefig("%s_%s_%s.png" %(var,grid_flag,flag), dpi=200); ann.remove()

def body(grid_flag,var):

	ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Tides/%s_zeta_MPDATA.nc' %(grid_flag), 'r', format='NETCDF4')
	ncdata2 = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Tides/Tides_Parent.nc', 'r', format='NETCDF4')

	ncdata3 = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Tides/%sc_zeta_MPDATA.nc' %(grid_flag), 'r', format='NETCDF4')
	ncdata4 = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Tides/Tides_Child.nc', 'r', format='NETCDF4')

	if var == 'zeta':
		w1 = ncdata1.variables['M2'][:]-ncdata2.variables['tide_Eamp'][0]
		w2 = ncdata3.variables['M2'][:]-ncdata4.variables['tide_Eamp'][0]
	elif var == 'uv':
		w1 = (ncdata1.variables['M2_u'][:]*ncdata1.variables['M2_u'][:]+ncdata1.variables['M2_v'][:]*ncdata1.variables['M2_v'][:])**0.5-ncdata2.variables['tide_Cmax'][0]
		w2 = (ncdata3.variables['M2_u'][:]*ncdata3.variables['M2_u'][:]+ncdata3.variables['M2_v'][:]*ncdata3.variables['M2_v'][:])**0.5-ncdata4.variables['tide_Cmax'][0]

	mintemp=-0.75; maxtemp=0.75; division=0.025
	clevs = np.arange(mintemp,maxtemp,division)
	cmap = cm.balance

	odys1 = pyroms.grid.get_ROMS_grid('Parent15')
	lons_p1, lats_p1 = odys1.hgrid.lon_rho, odys1.hgrid.lat_rho

	odys2 = pyroms.grid.get_ROMS_grid('Child15c')
	lons_p2, lats_p2 = odys2.hgrid.lon_rho, odys2.hgrid.lat_rho

	fig, ax, cax, m1 = grid_instance(llcrnrlon=-1, urcrnrlon=6, llcrnrlat=49, urcrnrlat=54.5, lat_ts=52, r='i', discr=1, caxx='vertical')
	xz,yz = bcz_bound()
	x, y = m1(xz, yz)
	m1.plot(x,y,color='black',linewidth=1.0)
	x1, y1 = m1(lons_p1, lats_p1)
	x2, y2 = m1(lons_p2, lats_p2)

	norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp)
	bounds=np.arange(mintemp,maxtemp+division,division)
	mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')

	PRINT_PNG(w1,w2,grid_flag,var,'YES',fig,m1,ax,x1,y1,x2,y2,clevs,cmap)
	PRINT_PNG(w1,w2,grid_flag,var,'NO',fig,m1,ax,x1,y1,x2,y2,clevs,cmap)


if __name__ == '__main__':
	name = ['OW','TW']
	var  = ['zeta','uv']

	body(name[0],var[0])
	body(name[1],var[0])
