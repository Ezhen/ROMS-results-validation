import matplotlib.pyplot as plt; import numpy as np; from netCDF4 import Dataset; from mpl_toolkits.basemap import Basemap; import matplotlib as mpl; from ezhen.plotbcz import *; import pyroms

name = ['OW','TW']; i=1
var  = ['zeta','uv']; n=1

ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/%s_%s.nc' %(name[i],var[n]), 'r', format='NETCDF4')
ncdata2 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/Tides_parent.nc', 'r', format='NETCDF4')

ncdata3 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/%sc_%s.nc' %(name[i],var[n]), 'r', format='NETCDF4')
ncdata4 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/Tide_nest.nc', 'r', format='NETCDF4')

if var[n] == 'zeta':
	w1 = ncdata1.variables['M2'][:]-ncdata2.variables['tide_Eamp'][0]
	w2 = ncdata3.variables['M2'][:]-ncdata4.variables['tide_Eamp'][0]
	mintemp=-0.75; maxtemp=0.75; division=0.025
elif var[n] == 'uv':
	w1 = (ncdata1.variables['M2_u'][:]*ncdata1.variables['M2_u'][:]+ncdata1.variables['M2_v'][:]*ncdata1.variables['M2_v'][:])**0.5-ncdata2.variables['tide_Cmax'][0]
	w2 = (ncdata3.variables['M2_u'][:]*ncdata3.variables['M2_u'][:]+ncdata3.variables['M2_v'][:]*ncdata3.variables['M2_v'][:])**0.5-ncdata4.variables['tide_Cmax'][0]
	mintemp=-0.75; maxtemp=0.75; division=0.025

clevs = np.arange(mintemp,maxtemp,division)
cmap=mpl.cm.jet #bwr
xyc='axes points'

odys1 = pyroms.grid.get_ROMS_grid('COARSEST')
lons_p1, lats_p1 = odys1.hgrid.lon_rho, odys1.hgrid.lat_rho

odys2 = pyroms.grid.get_ROMS_grid('FINER')
lons_p2, lats_p2 = odys2.hgrid.lon_rho, odys2.hgrid.lat_rho


def PRINT_PNG(w1,w2):
	CS1 = m1.contourf(x1,y1,w1,clevs,cmap=cmap)
	CS2 = m1.contourf(x2,y2,w2,clevs,cmap=cmap)
	ann = ax.annotate('M2', xy=(0,0),  xycoords=xyc,xytext=(325,20), textcoords=xyc,fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	fig.savefig("%s_%s.png" %(var[n],name[i]), dpi=200); ann.remove()


fig, ax, cax, m1 = grid_instance(llcrnrlon=-3, urcrnrlon=6, llcrnrlat=48, urcrnrlat=55, lat_ts=51.5, r='i', discr=1, caxx='vertical')
xz,yz = bcz_bound()
x, y = m1(xz, yz)
m1.plot(x,y,color='black',linewidth=1.0)
x1, y1 = m1(lons_p1, lats_p1)
x2, y2 = m1(lons_p2, lats_p2)

norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp)
bounds=np.arange(mintemp,maxtemp+division,division)
mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')


PRINT_PNG(w1,w2)

