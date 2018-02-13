"""
Script creates animation of physical parameter on chosen geographical area. Requirements: python with installed netcdf library and installed ffmpeg library.
Created by Evgeny Ivanov 11/04/2016
"""

from pylab import *
from netCDF4 import *
import datetime
import pylab
from mpl_toolkits.basemap import Basemap
import sys,os,shutil
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['axes.unicode_minus']=False

mpl.rc('font',family='Times New Roman')

dnsdatetime2py = lambda x: datetime.datetime(1981,1,1,0,0,0) + datetime.timedelta(seconds=x)
dnsdatetime2py2 = lambda x: datetime.datetime(2013,1,1,0,0,0) + datetime.timedelta(seconds=x)	 # conversion of ECMWF time into normal time
lo = lambda x: datetime.datetime(2013,1,1,0,0,0) + datetime.timedelta(days=x)


temp=np.zeros((365))

ncdata1 = Dataset('/home/eivanov/coawst_data_prrocessing/VERIFICATION_2013/IFREMER-NWS-SST-L4-NRT-OBS_FULL_TIME_SERIE_1476088307532.nc', 'r', format='NETCDF3')
lats = ncdata1.variables['lat'][:]
lons = ncdata1.variables['lon'][:]
time1 = ncdata1.variables['time'][:]#365
temp1 = ncdata1.variables['analysed_sst'][:,:,:]-273.15
mask = ncdata1.variables['mask'][:]
ncdata1.close()

def rms(lol):
	rms=np.zeros((365))
	ncdata2=Dataset(lol, 'r', format='NETCDF3')	# t[60]+(t[61]-t[60])/2=1306800.0 ; tt[30]*3600*24=1306800.0
	time2 = ncdata2.variables['time'][::4]#1455
	temp2 = ncdata2.variables['sst'][::4,:,:]
	ncdata2.close()
	jj=[]
	kk=[]
	for j in range(len(temp2[0,:,0])):
		for k in range(len(temp2[0,0,:])):
			if temp2[0,j,k]>0:
				if mask[0,j,k]==1:
					jj.append(j)
					kk.append(k)

	for i in range(0,364):
		temp11=[]
		temp22=[]
		temp33=[]
		for l in range(len(jj)):
			temp11.append(temp1[i,jj[l],kk[l]])
			temp22.append(temp2[i,jj[l],kk[l]])
			temp33.append((temp1[i,jj[l],kk[l]]-temp2[i,jj[l],kk[l]])**2)	# rms calculation (1)
		#rms[i]=sum(temp22)/len(temp22)-sum(temp11)/len(temp11)			# bias calculation
		rms[i]=(sum(temp33)/len(temp33))**0.5					# rms calculation (2)
		#print str(dnsdatetime2py(int(time1))), str(dnsdatetime2py2(int(time2)))
	return rms

fig = plt.figure()
ax = plt.subplot(111)
rms1=rms('/home/eivanov/Animation/Detidal_nudging/Replotting/Detidal.nc')
#rms2=rms('/home/eivanov/Animation/Detidal_nudging/Replotting/Tidal.nc')
#rms3=rms('/home/eivanov/Animation/Detidal_nudging/Replotting/tempPUSSY_u.nc')
#rms4=rms('/home/eivanov/Animation/Detidal_nudging/Replotting/tempPUSSY_b.nc')
plt.plot(np.linspace(1,364,364),rms1[0:364], 'g', linewidth=2.5)
#plt.plot(np.linspace(1,364,364),rms2[0:364], label='Tidal solution')
#plt.plot(np.linspace(1,364,364),rms3[0:364], label='Strong inflow and weak outflow nudging + Transparency of the North Sea')
#plt.plot(np.linspace(1,364,364),rms4[0:364], label='Weak nudging + Transparency of the North Sea')
pylab.xlim([1,364])
pylab.ylim([0,3])
plt.ylabel('RMS', fontsize=18)
yticks(linspace(0,3,7),fontsize=16)
xticks([15,44,74,104,135,165,195,226,257,287,318,348],[lo(30).strftime("%B"),lo(58).strftime("%B"),lo(89).strftime("%B"),lo(119).strftime("%B"),lo(150).strftime("%B"),lo(180).strftime("%B"),lo(211).strftime("%B"),lo(242).strftime("%B"),lo(272).strftime("%B"),lo(303).strftime("%B"),lo(333).strftime("%B"),lo(363).strftime("%B")],fontsize=16)
#vlines(31,0,3.5, linestyle='--', alpha=0.5);vlines(59,0,3.5, linestyle='--', alpha=0.5);vlines(90,0,3.5, linestyle='--', alpha=0.5);vlines(120,0,3.5, linestyle='--', alpha=0.5);vlines(151,0,3.5, linestyle='--', alpha=0.5);vlines(181,0,3.5, linestyle='--', alpha=0.5);vlines(212,0,3.5, linestyle='--', alpha=0.5); vlines(243,0,3.5, linestyle='--', alpha=0.5);vlines(273,0,3.5, linestyle='--', alpha=0.5);vlines(304,0,3.5, linestyle='--', alpha=0.5);vlines(334,0,3.5, linestyle='--', alpha=0.5)
vlines(31,-3,3, linestyle='--', alpha=0.5);vlines(59,-3,3, linestyle='--', alpha=0.5);vlines(90,-3,3, linestyle='--', alpha=0.5);vlines(120,-3,3, linestyle='--', alpha=0.5);vlines(151,-3,3, linestyle='--', alpha=0.5);vlines(181,-3,3, linestyle='--', alpha=0.5);vlines(212,-3,3, linestyle='--', alpha=0.5); vlines(243,-3,3, linestyle='--', alpha=0.5);vlines(273,-3,3, linestyle='--', alpha=0.5);vlines(304,-3,3, linestyle='--', alpha=0.5);vlines(334,-3,3, linestyle='--', alpha=0.5)
hlines(1.5, 1, 364, 'r', alpha=0.7)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True)

show()

