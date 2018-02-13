from pylab import *
from netCDF4 import *
import datetime
from mpl_toolkits.basemap import Basemap
import sys,os,shutil
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import calendar

dnsdatetime2py = lambda x: datetime.datetime(1981,1,1,0,0,0) + datetime.timedelta(seconds=x)
dnsdatetime2py2 = lambda x: datetime.datetime(2013,1,1,0,0,0) + datetime.timedelta(seconds=x)	 # conversion of ECMWF time into normal time
folder = os.path.abspath("Bias")

def PRINT_PNG(lats,lons,nx1,ny1,nx2,ny2,montemp,i,folder):
	tempo1 = m1.transform_scalar(montemp,lons,lats,nx1,ny1)
	tempo2 = m2.transform_scalar(montemp,lons,lats,nx2,ny2)
	#CS2 = m1.imshow(tempo1,cm.bwr,vmin=-2.5,vmax=2.5)
	#cb1 = colorbar(CS2, cax1, ticks=[-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5], orientation='horizontal') 
	#CS4 = m2.imshow(tempo2,cm.bwr,vmin=-2.5,vmax=2.5)
	#cb2 = colorbar(CS4, cax2, ticks=[-2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5],orientation='horizontal') 
	CS2 = m1.imshow(tempo1,cm.bwr,vmin=-3,vmax=3)
	cb1 = colorbar(CS2, cax1, ticks=[ -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3.0], orientation='horizontal') 
	CS4 = m2.imshow(tempo2,cm.bwr,vmin=-3,vmax=3)
	cb2 = colorbar(CS4, cax2, ticks=[ -3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3.0],orientation='horizontal') 
	m1.drawcountries()
	m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	m2.drawcountries()
	m2.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	file_name = os.path.abspath(folder+"/tmp"+str(i)+".png")
	fig.savefig(file_name, dpi=100)
	plt.close()

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 10))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, wspace=0.1)
plt.suptitle('Monthly mean bias: model minus satellite: Year',family='Courier New, monospace',fontsize=26, y=0.92)
ax1 = plt.subplot2grid((1,2), (0,0))
ax2 = plt.subplot2grid((1,2), (0,1))
m1 = Basemap(projection='merc',llcrnrlat=50,urcrnrlat=53.0,llcrnrlon=0,urcrnrlon=5,lat_ts=51.5,resolution='h', ax=ax1)
y_bcz=array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361])
x_bcz=array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
m1.drawparallels(arange(50,53,1),labels=[1,0,0,1],fontsize=10)
m1.drawmeridians(arange(0,5,1),labels=[1,0,1,0,1,0],fontsize=10)
m1.drawcoastlines()
m1.drawmapboundary(fill_color='#9999FF')
m2 = Basemap(projection='merc', llcrnrlat=51,urcrnrlat=51.9,llcrnrlon=2.0,urcrnrlon=3.5,lat_ts=51.45, resolution='f', ax=ax2)
m2.drawparallels(arange(51.0,51.9,0.3),labels=[1,0,0,0],fontsize=10)
m2.drawmeridians(arange(2,3.5,0.5),labels=[1,0,0,1],fontsize=10)
m2.drawcoastlines()
m2.drawmapboundary(fill_color='#9999FF')
divider1 = make_axes_locatable(ax1)
cax1 = divider1.append_axes("bottom", size=0.4, pad=0.15)
divider2 = make_axes_locatable(ax2)
cax2 = divider2.append_axes("bottom", size=0.4, pad=0.15)
ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/VERIFICATION_2013/IFREMER-NWS-SST-L4-NRT-OBS_FULL_TIME_SERIE_1476088307532.nc', 'r', format='NETCDF3')
ncdata2=Dataset('/home/eivanov/Animation/Detidal_nudging/Replotting/Detidal.nc', 'r', format='NETCDF3')	# t[60]+(t[61]-t[60])/2=1306800.0 ; tt[30]*3600*24=1306800.0
lats = ncdata1.variables['lat'][:]
lons = ncdata1.variables['lon'][:]
lon, lat=np.meshgrid(lons, lats)
x3, y3 = m1(x_bcz, y_bcz)
cs33 = m1.plot(x3,y3,color='black',linewidth=1.0)
x4, y4 = m2(x_bcz, y_bcz)
cs43 = m2.plot(x4,y4,color='black',linewidth=1.0)
nx1 = int((m1.xmax-m1.xmin)/301.)+1; ny1 = int((m1.ymax-m1.ymin)/150.)+1
nx2 = int((m2.xmax-m2.xmin)/301.)+1; ny2 = int((m2.ymax-m2.ymin)/150.)+1
time1 = ncdata1.variables['time'][:]
temp1 = ncdata1.variables['analysed_sst'][:,:,:]-273.15
time2 = ncdata2.variables['time'][:]
temp2 = ncdata2.variables['sst'][:,:,:]
ncdata1.close()
ncdata2.close()


time11=[]; n=1
montemp=np.zeros((len(temp1[0,:,0]),len(temp1[0,0,:])))
montemp1=np.zeros((len(temp1[0,:,0]),len(temp1[0,0,:])))
montemp2=np.zeros((len(temp2[0,:,0]),len(temp2[0,0,:])))
for i in range(len(time1)):
	if dnsdatetime2py(int(time1[i])).month==dnsdatetime2py(int(time1[i+1])).month:
		time11.append(i)
		print dnsdatetime2py(int(time1[i]))
	else:
		print dnsdatetime2py(int(time1[i]))
		print 'Calculation of the monthly averages'
		for k in range(len(temp1[0,:,0])):
			for l in range(len(temp1[0,0,:])):
				montemp1[k,l]=sum(temp1[time11[0]:time11[-1],k,l])/len(time11)
				montemp2[k,l]=sum(temp2[time11[0]:time11[-1],k,l])/len(time11)
				montemp[k,l]=montemp2[k,l]-montemp1[k,l]
		an = ax1.annotate('%s' %(calendar.month_name[dnsdatetime2py(int(time1[i])).month]), xy=(0,0),  xycoords='figure fraction',xytext=(430, 172), family='Courier New, monospace',textcoords='offset points',ha="left", va="bottom",fontsize=14, bbox=dict(width=90,facecolor='lightgrey', edgecolor='none', pad=5.0))
		PRINT_PNG(lats,lons,nx1,ny1,nx2,ny2,montemp,n,folder)
		time11=[]; n=n+1

n=0
montemp=np.zeros((len(temp1[0,:,0]),len(temp1[0,0,:])))
montemp1=np.zeros((len(temp1[0,:,0]),len(temp1[0,0,:])))
montemp2=np.zeros((len(temp2[0,:,0]),len(temp2[0,0,:])))
for i in range(len(time1)):
	for k in range(len(temp1[0,:,0])):
		for l in range(len(temp1[0,0,:])):
			montemp1[k,l]=sum(temp1[:,k,l])/len(time1)
			montemp2[k,l]=sum(temp2[:,k,l])/len(time1)
			montemp[k,l]=montemp2[k,l]-montemp1[k,l]
PRINT_PNG(lats,lons,nx1,ny1,nx2,ny2,montemp,n,folder)

