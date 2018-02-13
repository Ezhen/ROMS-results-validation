import matplotlib.pyplot as plt; import numpy as np; from netCDF4 import Dataset; from datetime import datetime, timedelta; from mpl_toolkits.basemap import Basemap
import matplotlib as mpl; import os, sys; import calendar;  from ezhen.plotbcz import *; from Func_Temp_Salt_VLIZ_stations import *; mpl.rcParams['legend.numpoints'] = 1; mpl.rcParams['legend.handlelength'] = 0
#plt.rcParams["font.family"] = 'Times New Roman'; mpl.rcParams['axes.unicode_minus']=False

var='salt' # 'temp','salt'
varr='sss' # 'sst', 'sss'
grid_name='OW'
#mintemp=4; maxtemp=20; division=0.25
mintemp=27; maxtemp=37; division=0.2

lv_name = ['120','130','215','230','330','435','700','710','780','ZG02']
lv_lat = [51.185,51.27083333,51.27666667,51.30833333,51.43333333,51.58066667,51.37666667,51.44083333,51.47116667,51.33333333]
lv_lon = [2.70116667,2.905,2.61333333,2.85,2.80833333,2.79033333,3.22,3.13866667,3.058,2.5]

lo = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)
folder = os.path.abspath("Animation/TempSalt")
cmap=mpl.cm.jet

clevs = np.arange(mintemp,maxtemp,division)
xyc='axes points'

ncdata1 = Dataset('Replotting/%s_bulk.nc' %(grid_name), 'r', format='NETCDF4')
ncdata2 = Dataset('Replotting/%sc_bulk.nc' %(grid_name), 'r', format='NETCDF4')
t=ncdata1.variables['time'][:]
sp_p=np.shape(ncdata1.variables[varr][0])
sp_c=np.shape(ncdata2.variables[varr][0])

mask_p=ncdata1.variables['mask_rho'][:]; mask_c=ncdata2.variables['mask_rho'][:]
lons_p, lats_p = ncdata1.variables['lon_rho'][:], ncdata1.variables['lat_rho'][:]
lons_c, lats_c = ncdata2.variables['lon_rho'][:], ncdata2.variables['lat_rho'][:]


#fig, ax, cax, m1 = grid_instance(llcrnrlon=0, urcrnrlon=4, llcrnrlat=50, urcrnrlat=53, lat_ts=51.5, r='i', discr=0.5, caxx='vertical')		# build the grid


roms_p=np.zeros((12,sp_p[0],sp_p[1]))
roms_c=np.zeros((12,sp_c[0],sp_c[1]))
day=np.zeros((12))

for i in range(len(t)):
	roms_p[lo(int(t[i])).month-1] = roms_p[lo(int(t[i])).month-1]+ncdata1.variables[varr][i,:,:]
	roms_c[lo(int(t[i])).month-1] = roms_c[lo(int(t[i])).month-1]+ncdata2.variables[varr][i,:,:]
	day[lo(int(t[i])).month-1] = day[lo(int(t[i])).month-1]+1

tt = func_lifewatch(var)
for n in range(12):
	fig, ax, cax, m1 = grid_instance(llcrnrlon=0.5, urcrnrlon=4.0, llcrnrlat=50.5, urcrnrlat=52.5, lat_ts=51.5, r='i', discr=0.5, caxx='vertical')
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
	ww_p = roms_p[n]/day[n]
	ww_c = roms_c[n]/day[n]
	w_p = np.ma.masked_where(abs(mask_p-1),ww_p)
	w_c = np.ma.masked_where(abs(mask_c-1),ww_c)
	CS1 = m1.ax.contourf(x1,y1,w_p,clevs,cmap=cmap)
	CS2 = m1.ax.contourf(x2,y2,w_c,clevs,cmap=cmap); lines=[]
	for i in range(10):
		xx,yy=m1(lv_lon[i],lv_lat[i])
		if tt[i,n]>0:
			lines.append(m1.plot(xx,yy,marker='o',color=cmap(round(float(tt[i,n]-mintemp)/(maxtemp-mintemp),2)),markersize=15,label=lv_name[i]))#,edgecolor='k')
	ann = ax.annotate('%s' %(calendar.month_name[n+1]), xy=(0,0),  xycoords=xyc,xytext=(275,20), textcoords=xyc,fontsize=20,  bbox=dict(facecolor='white',  edgecolor='none', pad=5.0))
	#aaa = ax.legend(title='LifeWatch',prop={'family':'Times New Roman','size':12},borderpad=2,handletextpad=1.5,labelspacing=1,loc=2,fontsize = 'large')
	#plt.setp(aaa.get_title(), fontsize=16, family='Times New Roman')
	file_name = os.path.abspath(folder + "/%s_%s_%s" %(grid_name,var,n+1)+".png"); print calendar.month_name[n+1]; fig.savefig(file_name, dpi=200); ann.remove()


