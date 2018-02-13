import matplotlib.pyplot as plt; import numpy as np; from netCDF4 import Dataset; from datetime import datetime, timedelta; from mpl_toolkits.basemap import Basemap
import matplotlib as mpl; import os, sys; import calendar;  from ezhen.plotbcz import *

lo = lambda x: datetime(1985,1,1,0,0,0) + timedelta(days=x)
folder = os.path.abspath("Animation/Currents/Month")
cmap=mpl.cm.jet
mintemp=0; maxtemp=0.35; division=0.01
clevs = np.arange(mintemp,maxtemp,division)
xyc='axes points'

PARAM = 'AV' # 'AV','INST'
prec = 1

if PARAM == 'AV':
	ncdata1 = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/TEMP_SALT_CURR_2004_2014.nc', 'r', format='NETCDF4')
elif PARAM == 'INST':
	ncdata1 = Dataset('Replotting/OWc_bulk.nc', 'r', format='NETCDF4')
t=ncdata1.variables['time'][:]; s = ncdata1.variables['votemper'][0,0]; sp=np.shape(s)
lon, lat = ncdata1.variables['lon'][:],ncdata1.variables['lat'][:]
mask=np.zeros((len(s),len(s.T)))
for i in range(len(mask)):
	for j in range(len(mask.T)):
		if s.mask[i,j]==False:
			mask[i,j]=1


def PRINT_PNG(u_m,v_m,rs_w,w,time):
	#tempo = m1.transform_scalar(w,lons_p[0],lats_p[:,0],nx,ny)
	#CS3 = m1.imshow(tempo,cmap,vmin=mintemp,vmax=maxtemp)
	CS3 = m1.contourf(x1,y1,rs_w,clevs,cmap=cmap)
	if PARAM=='AV':
		kk = m1.quiver(x1[::prec,::prec],y1[::prec,::prec],u_m[::prec,::prec],v_m[::prec,::prec],angles='xy')#,linewidth=rs_w[::prec,::prec].flatten(),angles='xy')
		monthname=calendar.month_name[time+1]
		ann = ax.annotate('%s' %(monthname), xy=(0,0),  xycoords=xyc,xytext=(275,20), textcoords=xyc,fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	if PARAM=='INST':
		kk = m1.quiver(x1[::prec,::prec],y1[::prec,::prec],u_m[::prec,::prec],v_m[::prec,::prec],linewidth=rs_w[::prec,::prec].flatten(),angles='xy')
		monthname=str(lo(time*60*60*24))#[0:10]
		ann = ax.annotate('%s' %(monthname), xy=(0,0),  xycoords=xyc,xytext=(175,20), textcoords=xyc,fontsize=20,  bbox=dict(facecolor='none',  edgecolor='none', pad=5.0))
	file_name = os.path.abspath(folder + "/Merc_%s_%s" %(time+1,monthname)+".png");  fig.savefig(file_name, dpi=80); ann.remove(); kk.remove() #; CS3.remove();


fig, ax, cax, m1 = grid_instance(llcrnrlon=0.5, urcrnrlon=3.6, llcrnrlat=50.5, urcrnrlat=52.5, lat_ts=51.5, r='i', discr=0.5, caxx='vertical')	# build the grid
#fig, ax, cax, m1 = grid_instance(llcrnrlon=0.5, urcrnrlon=6, llcrnrlat=48, urcrnrlat=55, lat_ts=-5, r='i', discr=1, caxx='vertical')	# build the grid
xz,yz = bcz_bound()
x, y = m1(xz, yz)
m1.plot(x,y,color='black',linewidth=1.0)
lons_p, lats_p = np.meshgrid(lon,lat)
x1, y1 = m1(lons_p, lats_p)
#nx = int((m1.xmax-m1.xmin)/2670.); ny = int((m1.ymax-m1.ymin)/3250.)

norm = mpl.colors.Normalize(vmin=mintemp, vmax=maxtemp)
bounds=np.arange(mintemp,maxtemp+division,division)
cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, boundaries=[-10] + bounds + [10], orientation='vertical')
cb.ax.set_title('m*s-1',family='times new roman')

roms=np.zeros((12,sp[0],sp[1]))
roms_u=np.zeros((12,sp[0],sp[1]))
roms_v=np.zeros((12,sp[0],sp[1]))

day=np.zeros((12))

if PARAM=='AV':
	a,b=0,12
	for i in range(731,731+365*3):#len(t)):
		roms[lo(int(t[i])).month-1] = roms[lo(int(t[i])).month-1]+ncdata1.variables['votemper'][i,0,:,:]
		roms_u[lo(int(t[i])).month-1] = roms_u[lo(int(t[i])).month-1]+ncdata1.variables['vozocrtx'][i,0,:,:]
		roms_v[lo(int(t[i])).month-1] = roms_v[lo(int(t[i])).month-1]+ncdata1.variables['vomecrty'][i,0,:,:]
		day[lo(int(t[i])).month-1] = day[lo(int(t[i])).month-1]+1
		print i
elif PARAM=='INST':
	a,b =154,156

for n in range(a,b):
	if PARAM=='AV':
		ru,rv = roms_u[n],roms_v[n]
		u10 = ru/day[n]
		v10 = rv/day[n]
		ww = roms[n]/day[n]-273.15
	elif PARAM=='INST':
		ru,rv = ncdata1.variables['ssu'][n,:,:],ncdata1.variables['ssv'][n,:,:]
		u10,v10 = np.flipud(ru),np.flipud(rv)
		ww = ncdata1.variables['sst'][n,:,:]
	roms_w_unmsk = (u10*u10+v10*v10)**0.5
	"""
	x2, y2 = m1(lons_p+rv, lats_p+ru)			# tricky algorythm, 
	u_map_unmsk, v_map_unmsk = x2-x1, y2-y1					# which I found in Internet
	mag_scale = np.hypot(u_map_unmsk, v_map_unmsk) / np.hypot(ru, rv)	# which rescales wind vectors
	u_map_unmsk /= mag_scale*1#0.1						# and makes them suitable
	v_map_unmsk /= mag_scale*1#0.1	
	u_map = np.ma.masked_where(abs(mask-1),u_map_unmsk)
	v_map = np.ma.masked_where(abs(mask-1),v_map_unmsk)
	"""
	#w = np.ma.masked_where(abs(mask-1),ww)
	#roms_w = np.ma.masked_where(abs(mask-1),roms_w_unmsk)
	#u_map,v_map = np.ma.masked_where(abs(mask-1),u10),np.ma.masked_where(abs(mask-1),v10)
	u_map,v_map,roms_w,w = u10,v10,roms_w_unmsk,ww
	PRINT_PNG(u_map,v_map,roms_w,w,n)
