import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from datetime import date, datetime, timedelta
from scipy import spatial
from Current_rose_VLIZ import current_rose_VLIZ
import sys
import math

lo2 = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)

def readtemp(line,n,k):
	try:
		a=round(float(line[n:k]),2)
	except:
		a='nan'
	return a


STAT = 3 #	Define Station number (1,2,3)

if STAT==1:
	f='/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20060101_20141231_MP0_Current.txt'; lat=51+23/60.+40.04/3600.; lon=3+2./60.+44.82/3600.
elif STAT==2:
	f='/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20060101_20141231_MP3_Current.txt'; lat=51+23/60.+22.57/3600.; lon=3+11/60.+55.42/3600.
else:
	f='/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20081001_20141231_MP4_Current.txt'; lat=51+25/60.+6.08/3600. ; lon=3+17/60.+54.88/3600.

t,ms,ds,ht=[],[],[],[]
for line in open(f,'r').readlines()[2::6]:
	a=line.split( )
	c=a[0]+' '+a[1]
	t.append(datetime.strptime(c, '%d/%m/%Y %H:%M'))
	ht.append(readtemp(line,18,25))
	ds.append(readtemp(line,28,34));   ms.append(readtemp(line,39,43)) 
	sys.stdout.write("Time: %s \r" % (t[-1]) ); sys.stdout.flush()
	if t[-1].year==2008 and t[-1].month==12 and t[-1].day==30:
		break


ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/NNuv.nc', 'r', format='NETCDF4')
lats = ncdata1.variables['lat_rho'][:]; lons = ncdata1.variables['lon_rho'][:]; times = ncdata1.variables['time'][:]; hs = ncdata1.variables['h'][:]; width=len(hs.T)
aa=np.array((list(lons.flatten()), list(lats.flatten()))).T


# And the corresponding ROMS locations
aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; 
idxx=spatial.KDTree(aa).query([lon,lat])[1]
a=int(idxx/width); b=int(idxx-(idxx/width)*width)


rt=[]
for i in range(len(times)):
	# converting roms time to datetime
	rt.append(lo2(int(times[i])))


tr,tv,rm,rd,m,d=[],[],[],[],[],[]
for i in range(len(t)):
	if ms[i] != 'nan' and ds[i] != 'nan':
		# find the corresponding ROMS time
		mini=min(rt,key=lambda x: abs(x-t[i]))
		index=rt.index(mini)
		tr.append(mini)
		tv.append(t[i])
		# print t[i], mini, index
		# find the corresponding ROMS lats and lons
		x=round(ncdata1.variables['ssu'][index,a,b],3)
		y=round(ncdata1.variables['ssv'][index,a,b],3)
		rmi=(x*x+y*y)**0.5
		rdi=round(math.radians(int(np.mod(math.degrees(math.atan2(x,y)),360))),2)
		rm.append(round(rmi,2))
		rd.append(rdi)
		m.append(round(ms[i],2))
		d.append(round(math.radians(ds[i]),2))
		print 'Time:', mini, 'R magn', rm[-1], 'R dir', rd[-1], 'V magn', m[-1], 'V dir', d[-1]

current_rose_VLIZ(np.array(m),np.array(d))
