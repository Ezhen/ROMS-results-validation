from pylab import *
from netCDF4 import *
import datetime
from mpl_toolkits.basemap import Basemap
import sys,os,shutil
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

dnsdatetime2py = lambda x: datetime.datetime(1981,1,1,0,0,0) + datetime.timedelta(seconds=x)
dnsdatetime2py2 = lambda x: datetime.datetime(2015,1,1,0,0,0) + datetime.timedelta(seconds=x)	 # conversion of ECMWF time into normal time
folder = os.path.abspath("Verification_side_by_side")

def PRINT_PNG(lats,lons,nx1,ny1,nx2,ny2,temp1,temp2,i,folder):
	#CS2 = m1.contourf(x1,y1,temp,clevs,cmap='bwr',animated=True)
	#CS4 = m2.contourf(x2,y2,temp,clevs,cmap='bwr',animated=True)
	#cb1 = colorbar(CS4, cax, orientation='horizontal') 
	tempo1 = m1.transform_scalar(temp1,lons,lats,nx1,ny1)
	tempo2 = m2.transform_scalar(temp2,lons,lats,nx2,ny2)
	CS2 = m1.imshow(tempo1,cm.coolwarm,vmin=4,vmax=17)
	cb1 = colorbar(CS2, cax1, ticks=[4,5,6,7,8,9,10,11,12,13,14,15,16,17], orientation='horizontal') 
	CS4 = m2.imshow(tempo2,cm.coolwarm,vmin=4,vmax=17)
	cb2 = colorbar(CS4, cax2, ticks=[4,5,6,7,8,9,10,11,12,13,14,15,16,17],orientation='horizontal') 
	m1.drawcountries()
	m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	m2.drawcountries()
	m2.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	file_name = os.path.abspath(folder+"/tmp"+str(i)+".png")
	fig.savefig(file_name, dpi=100)
	plt.close()

def body(l,n):
	ncdata1 = Dataset('/media/sf_Swap-between-windows-linux/VERIFICATION_SST.nc', 'r', format='NETCDF3')
	ncdata2=Dataset('/home/eivanov/coawst_data_prrocessing/FORCING/METEO/Replotting_into_regular_grid/tempPUSSY.nc', 'r', format='NETCDF3')	# t[60]+(t[61]-t[60])/2=1306800.0 ; tt[30]*3600*24=1306800.0
	lats = ncdata1.variables['lat'][:]
	lons = ncdata1.variables['lon'][:]
	lon, lat=np.meshgrid(lons, lats)
	#x1, y1 = m1(lon, lat)
	#x2, y2 = m2(lon, lat)
	x3, y3 = m1(x_bcz, y_bcz)
	cs33 = m1.plot(x3,y3,color='black',linewidth=1.0)
	x4, y4 = m2(x_bcz, y_bcz)
	cs43 = m2.plot(x4,y4,color='black',linewidth=1.0)
	nx1 = int((m1.xmax-m1.xmin)/301.)+1; ny1 = int((m1.ymax-m1.ymin)/150.)+1
	nx2 = int((m2.xmax-m2.xmin)/301.)+1; ny2 = int((m2.ymax-m2.ymin)/150.)+1
	i=0
	for i in range(n-l):
		time1 = ncdata1.variables['time'][l+i]#365
		temp1 = ncdata1.variables['analysed_sst'][l+i,:,:]-273.15
		time2 = ncdata2.variables['time'][(l+i)*4]#1455
		temp2 = ncdata2.variables['sst'][(l+i)*4,:,:]
		#temp=temp1-temp2
		#print np.shape(time1), np.shape(temp1), np.shape(time2), np.shape(temp2)
		print str(dnsdatetime2py(int(time1))), str(dnsdatetime2py2(int(time2)))
		an = ax1.annotate('%s' %(str(dnsdatetime2py(int(time1)))), xy=(0,0),  xycoords='figure fraction',xytext=(430, 172), family='Courier New, monospace',textcoords='offset points',ha="left", va="bottom",fontsize=14, bbox=dict(facecolor='lightgrey', edgecolor='none', pad=5.0))
		an = ax2.annotate('%s' %(str(dnsdatetime2py(int(time1)))), xy=(0,0),  xycoords='figure fraction',xytext=(912, 172), family='Courier New, monospace',textcoords='offset points',ha="left", va="bottom",fontsize=14, bbox=dict(facecolor='lightgrey', edgecolor='none', pad=5.0)) #840 170
		an = ax1.annotate('Satellite', xy=(0,0),  xycoords='figure fraction',xytext=(300, 70), family='Courier New, monospace',textcoords='offset points',ha="left", va="bottom",fontsize=20, bbox=dict(facecolor='none', edgecolor='none', pad=5.0))
		an = ax1.annotate('Model', xy=(0,0),  xycoords='figure fraction',xytext=(793, 70), family='Courier New, monospace',textcoords='offset points',ha="left", va="bottom",fontsize=20, bbox=dict(facecolor='none', edgecolor='none', pad=5.0))
   		#PRINT_PNG(x1,y1,x2,y2,temp,l+i,folder)
		PRINT_PNG(lats,lons,nx1,ny1,nx2,ny2,temp1,temp2,l+i,folder)
   		#print(str(l+i+1))
	ncdata1.close()
	ncdata2.close()

#for i in range(0,29):
for i in range(5,7):
	fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 10))
	plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, wspace=0.1)
	plt.suptitle('Difference in sea surface temperature',family='Courier New, monospace',fontsize=26, y=0.92)
	ax1 = plt.subplot2grid((1,2), (0,0))
	ax2 = plt.subplot2grid((1,2), (0,1))
	m1 = Basemap(projection='merc',llcrnrlat=50,urcrnrlat=53.0,llcrnrlon=0,urcrnrlon=5,lat_ts=51.5,resolution='h', ax=ax1)
	y_bcz=array([51.37361, 51.37361, 51.37268, 51.33611, 51.32416, 51.31485, 51.27638, 51.24972, 51.21334, 51.09403, 51.09111, 51.09111, 51.09111, 51.09361, 51.09433, 51.26917, 51.55472, 51.55777, 51.55777, 51.61306, 51.61306, 51.80500, 51.87000, 51.87000, 51.55167, 51.48472, 51.45000, 51.37944, 51.37361, 51.37361])
	x_bcz=array([3.36472, 3.36472, 3.36491, 3.17972, 3.13166, 3.10403, 3.02000, 2.95528, 2.86305, 2.55555, 2.54166, 2.54166, 2.54166, 2.54361, 2.54298, 2.39028, 2.23973, 2.23812, 2.23812, 2.25333, 2.25333, 2.48167, 2.53944, 2.53944, 3.08139, 3.21222, 3.29639, 3.35389, 3.36472, 3.36472])
	m1.drawparallels(arange(50,53,1),labels=[1,0,0,1],fontsize=10)
	m1.drawmeridians(arange(0,5,1),labels=[1,0,1,0,1,0],fontsize=10)
	m1.drawcoastlines()
	m1.drawmapboundary(fill_color='#9999FF')
	m2 = Basemap(projection='merc',llcrnrlat=50,urcrnrlat=53.0,llcrnrlon=0,urcrnrlon=5,lat_ts=51.5,resolution='h', ax=ax2)
	m2.drawparallels(arange(50,53,1),labels=[1,0,0,1],fontsize=10)
	m2.drawmeridians(arange(0,5,1),labels=[1,0,1,0,1,0],fontsize=10)
	m2.drawcoastlines()
	m2.drawmapboundary(fill_color='#9999FF')
	#cax = fig.add_axes([0.2, 0.08, 0.6, 0.04])
	divider1 = make_axes_locatable(ax1)
	cax1 = divider1.append_axes("bottom", size=0.4, pad=0.15)
	divider2 = make_axes_locatable(ax2)
	cax2 = divider2.append_axes("bottom", size=0.4, pad=0.15)
	body(50*i,50+50*i)
body(350,364)
