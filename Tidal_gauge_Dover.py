import numpy as np; import matplotlib.pyplot as plt; import matplotlib as mpl; import re; from datetime import date, datetime, timedelta; from netCDF4 import Dataset;from scipy import spatial; from dateutil.relativedelta import relativedelta; mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman'); lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(days=x)

lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(days=x)
lon_tide=1.322667; lat_tide=51.114389 # Tidal gauge coordinates: 51.114389 & 1.322667

#ncdata1 = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Interannual_results_tides/his_t_5.nc', 'r', format='NETCDF3')
ncdata1 = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Interannual_results_tides/avg_t_55.nc', 'r', format='NETCDF3')
lats = ncdata1.variables['lat_rho'][:]; lons = ncdata1.variables['lon_rho'][:]; times = ncdata1.variables['ocean_time'][:]; times=times/24/60/60.
aa=np.array((list(lons.flatten()), list(lats.flatten()))).T
mask=0
#	Iteration, that permits to find the closest geographical point, if it is unmasked
while mask==0: 
	idxx=spatial.KDTree(aa).query([lon_tide,lat_tide])[1]; lon1=aa[idxx][0]; lat1=aa[idxx][1]
	h = ncdata1.variables['h'][:].flatten()[idxx]; mask = int(ncdata1.variables['mask_rho'][:].flatten()[idxx])
	if mask==0:
		aa[idxx][0]=-999;aa[idxx][1]=-999 
	print lon1, lat1, h, mask

def find_nearest(array,value):
	idx = (np.abs(array-value)).argmin(); #print t[i]*24*60*60, array[idx]
	return array[idx], idx

time=[]; a=[]; time1=[]; time2=[]; zetas=[]; mm=0; sumzet=0
for line in open('Tidal_gauge.txt','r'):
	time.append(float(line.split("\t")[0])); a.append(float(line.split("\t")[1]))
zeta=np.array(a); zeta[zeta==-99999]='NaN'; zeta=zeta/1000.

#	use only in case of instant data !!!
'''
for i in range(len(times)):	
	days=(lo(times[i])-datetime(lo(times[i]).year, 1, 1, 1, 1)).days; seconds=(lo(times[i])-datetime(lo(times[i]).year, 1, 1, 1, 1)).seconds/60/60/24.; frac=days+seconds
	year=2004+relativedelta(lo(times[i]), lo(times[0])).years
	if lo(times[i]).year==2004 or lo(times[i]).year==2008 or lo(times[i]).year==2012:
		time1.append(round(year + frac/366.,4))
	else:
		time1.append(round(year + frac/365.,4))

for i in range(len(time)):
	time2.append(find_nearest(np.array(time1),time[i])[0])
	idx=find_nearest(np.array(time1),time[i])[1]
	zetas.append(ncdata1.variables['zeta'][idx,int(np.where(lons==lon1)[0][0]),int(np.where(lons==lon1)[1][0])])
'''

for i in range(len(times)-1):
	print i
	if lo(times[i]).month==lo(times[i+1]).month:
		sumzet=sumzet+ncdata1.variables['zeta'][i,int(np.where(lons==lon1)[0][0]),int(np.where(lons==lon1)[1][0])]; mm=mm+1
	else:
		zetas.append(sumzet/mm); sumzet=0;mm=0
	


fig=plt.figure(figsize=(20, 12))#; plt.suptitle(var[m],family='Courier New, monospace',fontsize=20, y=0.88)
plt.plot(time[0:-1],zeta[0:-1], 'r', linewidth=3, label='Dover (Tidal gauge)')
plt.plot(time[0:-1],4+np.array(zetas), 'b', linewidth=3, label='ROMS')
plt.xticks(np.linspace(2004,2014,11),fontsize=16)
plt.xlim(2004,2014); plt.ylim(3,5); plt.ylabel('Sea surface elevation [m]', fontsize=20); plt.xlabel('Year', fontsize=20); plt.legend(loc=1,prop={'size':18}); plt.hlines(0, 0, 12, linestyle='--', alpha=0.7, linewidth=1.0); plt.yticks(np.linspace(3,5,9),fontsize=16)#; plt.show()
fig.savefig('Tidal_gauge_Dover', dpi=200); print 'Figure Tidal_gauge_Dover is saved'



