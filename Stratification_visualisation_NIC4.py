#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import datetime
from netCDF4 import Dataset
import matplotlib
import sys
sys.path.insert(0, '../cmocean')
import cmocean.cm as cm

d2 = lambda x: datetime.datetime(2006,1,1,0,0,0) + datetime.timedelta(seconds=x)


def plotfig(m,flag,path,grid_flag,profile):
	n1 = Dataset(path, 'r', format='NETCDF4')
	t = n1.variables['ocean_time'][m]
	var = n1.variables[flag][m,:,profile,:]
	h = n1.variables['h'][profile,:]
	c = n1.variables['Cs_r'][:]

	xi = np.arange(len(h))
	x = np.tile(xi,15)
	y=[]

	for j in range(15):
		for i in range(len(h)):
			y.append(h[i]*c[j])

	y = np.array(y)*(-1)

	yi = np.linspace(0,55,23)
	zi = matplotlib.mlab.griddata(x, y , var.flatten(), xi, yi, interp='linear')

	if flag == 'temp':
		lev = np.linspace(3,21,37)
		label = 'Temperature [$^\circ$C]'
		color = cm.thermal
	else:
		lev = np.linspace(12,40,57)
		label = 'Salinity [PSU]'
		color = cm.haline

	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 7))

	plt.gca().patch.set_color('silver')
	CS1 = plt.contourf(xi,yi,zi, levels = lev, cmap = cm.thermal)
	if flag == 'temp':
		CS2 = plt.contour(xi,yi,zi,linewidths = 0.5, levels = lev[::2], colors='k')
	if flag == 'salt':
		CS2 = plt.contour(xi,yi,zi,linewidths = 0.5, levels = lev[::2], colors='k')
	plt.clabel(CS2, inline=1, fmt='%1.1f', fontsize=10)
	plt.colorbar(CS1, orientation='horizontal', label=label)

	plt.ylim(50,0)
	if grid_flag == 'NN' or grid_flag == 'OW' or grid_flag == 'TW':
		plt.xlim(15,82)
	else:
		plt.xlim(7,136)
	#plt.xlabel("Coordinates")
	plt.ylabel("Depth [m]")

	labels = [item.get_text() for item in ax.get_xticklabels()]
	for i in (1,-2):
		lg =  '(' + str(np.round(n1.variables['lat_rho'][profile,i],2)) + '$^\circ$N,  ' +  str(np.round(n1.variables['lon_rho'][profile,i],2))
		if n1.variables['lon_rho'][profile,i] > 0 :
			lg = lg + '$^\circ$E)'
		else:
			lg = lg + '$^\circ$W)'
		labels[i] = lg
	ax.set_xticklabels(labels)

	name = d2(t).strftime("%d %B %Y")
	ax.annotate('%s' %(name), xy=(0,0), xycoords='axes points',xytext=(550,15), fontsize=12,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))

	fig.savefig('Stratification_images/Stratification_' + grid_flag + '_' + flag + '_' + d2(t).strftime("%d_%B_%Y") + '.png', dpi=200)




if __name__ == '__main__':
	#Choose one of those: path to the file, name of the grid, location of the profile which has a connection to Scheldt
	#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSSNNHIS_20062008.nc'; grid_flag = 'NN'; profile = 37
	path1 = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_HIS_20062008_parent.nc'#; grid_flag = 'OW'; profile = 37
	path2 = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_HIS_20062008_parent.nc'#; grid_flag = 'TW'; profile = 37
	path3 = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_HIS_20062008_child.nc'#; grid_flag = 'OWc'; profile = 11
	path4 = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_HIS_20062008_child.nc'#; grid_flag = 'TWc'; profile = 11

	# moment of time
	moment = [24*45, 24*134, 24*226, 24*318] # Feb, May, Aug, Nov
	path_all = np.array([path1,path2,path3,path4])
	grid_flag_all = np.array(['OW','TW','OWc','TWc'])
	profile_all = np.array([37,37,11,11])

	for i in range(len(moment)):
		m = moment[i]
		for j in range(len(path_all)):
			# flag, choose one of those or both
			plotfig(m,'temp',path_all[j],grid_flag_all[j],profile_all[j])
			plotfig(m,'salt',path_all[j],grid_flag_all[j],profile_all[j])
