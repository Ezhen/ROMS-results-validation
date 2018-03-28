import numpy as np; import matplotlib.pyplot as plt; from netCDF4 import Dataset; from datetime import date, datetime, timedelta; from scipy import spatial; import re; from functions import find_nearest
lo = lambda x: datetime(2006,1,1,0,0,0) + timedelta(days=x); lo2 = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)

ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/NN.nc', 'r', format='NETCDF4')
lats = ncdata1.variables['lat_rho'][:]; lons = ncdata1.variables['lon_rho'][:]; times = ncdata1.variables['time'][:]; hs = ncdata1.variables['h'][:];aa=np.array((list(lons.flatten()), list(lats.flatten()))).T

stat,time,lat,lon,salt,temp,t,rt,ridx,sstR,sssR=[],[],[],[],[],[],[],[],[],[],[]; width=len(hs.T)

for line in open('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/Data_Vliz_Temp_Salinity','r').readlines()[1:]:
	# reading a file
	stat1 = line.split("\t")[0].split('"')[1]
	date1 = re.split('-| |:', line.split("\t")[1])
	a = line.split("\t")
	lat1,lon1,salt1,temp1 = a[2], a[3],a[15],a[29]
	if int(date1[0])>2005 and int(date1[0])<2009 and salt1!='NA' and temp1!='NA':
		# excluding from appending missing values and times out of the chosen simulation time frame 2006-2008
		stat.append(stat1)
		t.append(datetime(int(date1[0]),int(date1[1]),int(date1[2]),int(date1[3])))
		lat.append(float(lat1)),lon.append(float(lon1)),salt.append(float(salt1)),temp.append(float(temp1))

for i in range(len(times)):
	# converting roms time to datetime
	rt.append(lo2(int(times[i])))

for i in range(len(t)):
	# find the corresponding ROMS time
	mini=min(rt,key=lambda x: abs(x-t[i]))
	index=rt.index(mini)
	ridx.append(index)
	#print t[i], mini, index
	# find the corresponding ROMS lats and lons
	idxx=spatial.KDTree(aa).query([lon[i],lat[i]])[1]
	a=int(idxx/width)
	b=int(idxx-(idxx/width)*width)
	sstR.append(ncdata1.variables['sst'][index,a,b])
	sssR.append(ncdata1.variables['sss'][index,a,b])
	print i
	print '       Time:', 'VLIZ:', t[i], 'ROMS:', mini
	print '   Location:', 'VLIZ:', '(',round(lat[i],2),',',round(lon[i],2),')', 'ROMS:', '(',round(lats[a,b],2),',',round(lons[a,b],2),')'
	print 'Temperature:', 'VLIZ:', round(temp[i],1), 'ROMS', round(sstR[-1],1)
	print '   Salinity:', 'VLIZ:', round(salt[i],1), 'ROMS', round(sssR[-1],1)

def coeff(r,o,lenth,name):
	# Calculate metrics #
	# 'r' - results to be validated, 'o' - validation array, 'lenth' - lenth of the array, 'name' - name of the array #
	aa=sum((o-r)**2); bb=sum((o-np.mean(o))**2)
	ntcf=1-(aa/bb)
	bias=np.mean(r-o)
	rms=(np.sum((r-o)**2)/(lenth))**0.5
	return bias,rms,ntcf

# Average array without partition on stations and months #
bsT,rsT,ntT = coeff(np.array(sstR),np.array(temp),len(temp),'Temp total-averages:')
bsS,rsS,ntS = coeff(np.array(sssR),np.array(salt),len(salt),'Salt total-averages:')
print 'Temp total-averages:', 'bias', round(bsT,2), 'rms', round(rsT,2), 'nash-sutcliffe coeff', round(ntT,2)
print 'Salt total-averages:', 'bias', round(bsS,2), 'rms', round(rsS,2), 'nash-sutcliffe coeff', round(ntS,2)

# Station average #
statU = [[] for i in range(len(np.unique(stat)))]; k=0
lstVT,lstVS = [[] for i in range(len(np.unique(stat)))],[[] for i in range(len(np.unique(stat)))]
lstRT,lstRS = [[] for i in range(len(np.unique(stat)))],[[] for i in range(len(np.unique(stat)))]

statU[k].append(stat[0]); dd = len(statU)
lstVT[k].append(temp[0]); lstVS[k].append(salt[0])
lstRT[k].append(sstR[0]); lstRS[k].append(sssR[0])

for i in range(1,len(temp)):
	if stat[i] == stat[i-1]:
		lstVT[k].append(temp[i]); lstVS[k].append(salt[i])
		lstRT[k].append(sstR[i]); lstRS[k].append(sssR[i])
	else:
		k=k+1
		statU[k].append(stat[i])
		lstVT[k].append(temp[i]); lstVS[k].append(salt[i])
		lstRT[k].append(sstR[i]); lstRS[k].append(sssR[i])

bsT,rsT,ntT,bsS,rsS,ntS=[],[],[],[],[],[]
for i in range(dd):
	u1,v1,z1=coeff(np.array(lstRT[i]),np.array(lstVT[i]),len(lstVT[i]),'Temp station-averages:')
	u2,v2,z2=coeff(np.array(lstRS[i]),np.array(lstVS[i]),len(lstVS[i]),'Salt station-averages:')
	bsT.append(u1); rsT.append(v1); ntT.append(z1)
	bsS.append(u2); rsS.append(v2); ntS.append(z2)

print 'Temp station-averages:', 'bias', round(sum(bsT)/len(bsT),2), 'rms', round(sum(rsT)/len(rsT),2), 'nash-sutcliffe coeff', round(sum(ntT)/len(ntT),2)
print 'Salt station-averages:', 'bias', round(sum(bsS)/len(bsS),2), 'rms', round(sum(rsS)/len(rsS),2), 'nash-sutcliffe coeff', round(sum(ntS)/len(ntS),2)



# Monthly average #
lstVTy,lstVSy = [[] for i in range(12)],[[] for i in range(12)]
lstRTy,lstRSy = [[] for i in range(12)],[[] for i in range(12)]

for i in range(len(temp)):
	y=int(t[i].month-1)
	lstVTy[y].append(temp[i]); lstVSy[y].append(salt[i])
	lstRTy[y].append(sstR[i]); lstRSy[y].append(sssR[i])

bsyT,rsyT,ntyT,bsyS,rsyS,ntyS=[],[],[],[],[],[]
for i in range(12):
	u1,v1,z1=coeff(np.array(lstRTy[i]),np.array(lstVTy[i]),len(lstVTy[i]),'Temp monthly-averages:')
	u2,v2,z2=coeff(np.array(lstRSy[i]),np.array(lstVSy[i]),len(lstVSy[i]),'Salt monthly-averages:')
	bsyT.append(u1); rsyT.append(v1); ntyT.append(z1)
	bsyS.append(u2); rsyS.append(v2); ntyS.append(z2)

print 'Temp monthly-averages:', 'bias', round(sum(bsyT)/len(bsyT),2), 'rms', round(sum(rsyT)/len(rsyT),2), 'nash-sutcliffe coeff', round(sum(ntyT)/len(ntyT),2)
print 'Salt monthly-averages:', 'bias', round(sum(bsyS)/len(bsyS),2), 'rms', round(sum(rsyS)/len(rsyS),2), 'nash-sutcliffe coeff', round(sum(ntyS)/len(ntyS),2)


