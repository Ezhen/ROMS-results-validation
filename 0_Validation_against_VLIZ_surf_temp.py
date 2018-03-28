import numpy as np; import matplotlib.pyplot as plt; from netCDF4 import Dataset; from datetime import date, datetime, timedelta; from scipy import spatial; import re; from functions import find_nearest
lo = lambda x: datetime(2006,1,1,0,0,0) + timedelta(days=x); lo2 = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)


def readtemp(line,n,k):
	try:
		a=round(float(line[n:k]),2)
	except:
		a='nan'
	return a


def coeff(rr,oo,lenth):
	# Calculate metrics #
	# 'r' - results to be validated, 'o' - validation array, 'lenth' - lenth of the array #
	r,o=[],[]
	for i in range(lenth):
		if oo[i] != 'nan':
			r.append(float(rr[i]))
			o.append(float(oo[i]))
	lenth=len(r)
	r=np.array(r); o=np.array(o)
	aa=sum((o-r)**2); bb=sum((o-np.mean(o))**2)
	ntcf=1-(aa/bb)
	bias=np.mean(r-o)
	rms=(np.sum((r-o)**2)/(lenth))**0.5
	return bias,rms,ntcf


t,st1,st2,st3=[],[],[],[]
for line in open('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20060101_20141231_Seawater_Temperature.txt','r').readlines()[2::6]:
	# reading theVLIZ file with water temperatures
	a=line.split( )
	c=a[0]+' '+a[1]
	t.append(datetime.strptime(c, '%d/%m/%Y %H:%M'))
	st1.append(readtemp(line,20,25))
	st2.append(readtemp(line,29,34))
	st3.append(readtemp(line,38,43))
	if t[-1].year==2008 and t[-1].month==12 and t[-1].day==30:
		break


ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/NN.nc', 'r', format='NETCDF4')
lats = ncdata1.variables['lat_rho'][:]; lons = ncdata1.variables['lon_rho'][:]; times = ncdata1.variables['time'][:]; hs = ncdata1.variables['h'][:]; width=len(hs.T)
aa=np.array((list(lons.flatten()), list(lats.flatten()))).T


rt=[]
for i in range(len(times)):
	# converting roms time to datetime
	rt.append(lo2(int(times[i])))


# VLIZ stations locations
MP0_lat=51+23/60.+40.04/3600.; MP0_lon=3+2./60.+44.82/3600. # MP0 (Measuring Pile 0, Oostdyckbank)
MP3_lat=51+23/60.+22.57/3600.; MP3_lon=3+11/60.+55.42/3600. # MP3 (Measuring Pile 3, Westhinder)  
MP4_lat=51+25/60.+6.08/3600. ; MP4_lon=3+17/60.+54.88/3600. # MP4 (Measuring Pile 4, Westhinder)


# And the corresponding ROMS locations
aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; 
idxx=spatial.KDTree(aa).query([MP0_lon,MP0_lat])[1]; idxx3=spatial.KDTree(aa).query([MP3_lon,MP3_lat])[1]; idxx4=spatial.KDTree(aa).query([MP4_lon,MP4_lat])[1]; 
a0=int(idxx/width); b0=int(idxx-(idxx/width)*width); a3=int(idxx3/width); b3=int(idxx3-(idxx3/width)*width); a4=int(idxx4/width); b4=int(idxx4-(idxx4/width)*width)


ridx,sr1,sr2,sr3=[],[],[],[]
for i in range(len(t)):
	# find the corresponding ROMS time
	mini=min(rt,key=lambda x: abs(x-t[i]))
	index=rt.index(mini)
	ridx.append(index)
	# print t[i], mini, index
	# find the corresponding ROMS lats and lons
	sr1.append(round(ncdata1.variables['sst'][index,a0,b0],2))
	sr2.append(round(ncdata1.variables['sst'][index,a3,b3],2))
	sr3.append(round(ncdata1.variables['sst'][index,a4,b4],2))
	print '       Time:', 'VLIZ:', t[i], 'ROMS:', mini
	print 'Temp MP0:', 'VLIZ:', st1[i], 'ROMS', sr1[-1]
	print 'Temp MP3:', 'VLIZ:', st2[i], 'ROMS', sr2[-1]
	print 'Temp MP4:', 'VLIZ:', st3[i], 'ROMS', sr3[-1]

bsT,rsT,ntT = coeff(np.array(sr1),np.array(st1),len(sr1))
print 'Temp MP0', 'bias', round(bsT,2), 'rms', round(rsT,2), 'nash-sutcliffe coeff', round(ntT,2)


bsT,rsT,ntT = coeff(np.array(sr2),np.array(st2),len(sr2))
print 'Temp MP3', 'bias', round(bsT,2), 'rms', round(rsT,2), 'nash-sutcliffe coeff', round(ntT,2)


bsT,rsT,ntT = coeff(np.array(sr3),np.array(st3),len(sr3))
print 'Temp MP4', 'bias', round(bsT,2), 'rms', round(rsT,2), 'nash-sutcliffe coeff', round(ntT,2)

