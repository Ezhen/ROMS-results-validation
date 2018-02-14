from netCDF4 import Dataset; import numpy as np; import datetime; d = lambda x: datetime.datetime(1900,1,1,0,0,0) + datetime.timedelta(hours=x); d2 = lambda x: datetime.datetime(2004,1,1,0,0,0) + datetime.timedelta(seconds=x); import matplotlib.pyplot as plt; import matplotlib as mpl; mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman')
from scipy.stats import pearsonr

romsvar=['sst','swrad','lwr','latent','sensible', 'evaporation', 'shflux', 'ssflux']; esmwf=['sst','ssr','str','slhf','sshf','e']

k=1; ymin,ymax,al=-2,2,0.5; b1,b2,b3=91*k,182*k,274*k; maxx=365*k; # k -scale factor

rr = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo_Climatology/Meteo_2004_all_improved.nc', 'r', format='NETCDF4')
hh = Dataset('/media/sf_Swap-between-windows-linux/Tides/Meteo/Meteo_2004_all.nc', 'r', format='NETCDF4')
#nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/CLOUDS_Fluxes_Replotted.nc', 'r', format='NETCDF4'); msk2 = nc.variables['lwr'][0,:,:]
#fg = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/CLOUD_TEMP.nc', 'r', format='NETCDF4'); msk2 = nc.variables['lwr'][0,:,:]
nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/Good_humid_all_fluxes.nc', 'r', format='NETCDF4'); msk2 = nc.variables['lwr'][0,:,:]
fg = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/TEMP_GOOD_HUMIDITY.nc', 'r', format='NETCDF4')
tr = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/SALT_HUMIDITY.nc', 'r', format='NETCDF4')
sg = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Odyssea_Replotting/analysed_sstECMWF.nc', 'r', format='NETCDF4')
hf = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Meteo_coastline_shifted/Climatology_Meteo.nc', 'r', format='NETCDF4')

maska=np.zeros((len(msk2),len(msk2.T)))

ff = Dataset('/media/sf_Swap-between-windows-linux/Climatology_Meteo.nc', 'r', format='NETCDF3'); msk = ff.variables['sst'][0,:,:]; 
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if type(msk[i,j]) != np.ma.core.MaskedConstant and msk2[i,j] != 0 and j>11:
			maska[i,j]=1
count=np.sum(maska); ff.close()
"""
sfx=np.zeros((maxx)); r=np.zeros((maxx)); e=np.zeros((maxx))
for i in range(len(sfx)): 
	roms_unmasked=nc.variables['sensible'][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	esmf_unmasked=np.sum(rr.variables['sshf'][8*i:8*i+8],axis=0)/8;esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	sfx[i]=r[i]-e[i]; print i,r[i],e[i],e[i]/r[i]

lwr=np.zeros((maxx)); r=np.zeros((maxx)); e=np.zeros((maxx))
for i in range(len(sfx)): 
	roms_unmasked=nc.variables['lwr'][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	esmf_unmasked=np.sum(rr.variables['str'][8*i:8*i+8],axis=0)/8;esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	lwr[i]=r[i]-e[i]; print i,r[i],e[i],e[i]/r[i]

lfx=np.zeros((maxx)); r=np.zeros((maxx)); e=np.zeros((maxx))
for i in range(len(lfx)): 
	roms_unmasked=nc.variables['latent'][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	esmf_unmasked=np.sum(rr.variables['slhf'][8*i:8*i+8],axis=0)/8;esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	lfx[i]=r[i]-e[i]; print i,r[i],e[i],e[i]/r[i]

ww=np.zeros((maxx))
for i in range(len(ww)): 
	esmf_unmasked=((np.sum(rr.variables['u10'][8*i:8*i+8],axis=0)/8)**2+(np.sum(rr.variables['u10'][8*i:8*i+8],axis=0)/8)**2)**0.5;esmf=np.ma.masked_where(maska==0,esmf_unmasked); ww[i]=np.sum(esmf)/count

sst=np.zeros((maxx)); r=np.zeros((maxx)); e=np.zeros((maxx))
for i in range(len(r)): 
	esmf_unmasked=-273.15+hh.variables['t2m'][i*8];esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	roms_unmasked=fg.variables['sst'][i*24]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	sst[i]=r[i]-e[i]
"""
"""
sssww=np.copy(lfx);ssslfx=np.copy(lfx);ssssfx=np.copy(lfx)
for i in range(7,len(ww)-7):
	ssssfx[i]=sum(sfx[i-7:i+7])/14.; ssslfx[i]=sum(lfx[i-7:i+7])/14.; sssww[i]=sum(ww[i-7:i+7])/14.
"""
corr_ww_lw,corr_ww_lt,corr_ww_ss,=np.zeros((len(msk2),len(msk2.T))),np.zeros((len(msk2),len(msk2.T))),np.zeros((len(msk2),len(msk2.T))); rrr=len(nc.variables['sensible'][:]); lenn=rrr*8; fgg=lenn; ww,ess_avg,elt_avg,elf_avg=np.zeros((lenn/8)),np.zeros((lenn/8)),np.zeros((lenn/8)),np.zeros((lenn/8))
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if maska[i,j]==1:
			### Sensible ###
			rss=nc.variables['sensible'][:,i,j]
			for k in range(lenn/8):
				ess_avg[k]=sum(rr.variables['sshf'][8*i:8*i+8,i,j])/8.
			ss=rss-ess_avg
			### Latent ###
			rlt=nc.variables['latent'][:,i,j]
			for k in range(lenn/8):
				elt_avg[k]=sum(rr.variables['slhf'][8*i:8*i+8,i,j])/8.
			lt=rlt-elt_avg
			### Longwave ###
			rlf=nc.variables['lwr'][:,i,j]
			for k in range(lenn/8):
				elf_avg[k]=sum(rr.variables['str'][8*i:8*i+8,i,j])/8.
			lw=rlf-elf_avg
			### Wind ###
			for k in range(lenn/8):
				#ww[k]=sum((rr.variables['u10'][8*k:8*k+8,i,j]**2+rr.variables['v10'][8*k:8*k+8,i,j]**2)**0.5)/8.
				#ww[k]=sum(rr.variables['d2m'][8*k:8*k+8,i,j])/8.
				#ww[k]=sum(rr.variables['tcc'][8*k:8*k+8,i,j])/8.
				### SST ###
				#ww[k]=fg.variables['sst'][24*k,i,j]+273.15-sg.variables['sst'][k,i,j]
				#ww[k]=hf.variables['sst'][4*k,i,j]-273.15
				ww[k]=tr.variables['salt'][24*k,i,j]
			#temp[i,j]=rt[i,j]-et[i,j]
			corr_ww_lw[i,j]=np.corrcoef(ww,lw)[0][1]
			corr_ww_lt[i,j]=np.corrcoef(ww,lt)[0][1]
			corr_ww_ss[i,j]=np.corrcoef(ww,ss)[0][1]
			print i,j,corr_ww_lt[i,j],corr_ww_lw[i,j],corr_ww_ss[i,j]
correl_ww_lw=np.ma.masked_where(maska==0,corr_ww_lw);correlation_ww_lw=np.sum(correl_ww_lw)/count
correl_ww_lt=np.ma.masked_where(maska==0,corr_ww_lt);correlation_ww_lt=np.sum(correl_ww_lt)/count
correl_ww_ss=np.ma.masked_where(maska==0,corr_ww_ss);correlation_ww_ss=np.sum(correl_ww_ss)/count
print 'wind-longwave',correlation_ww_lw,'wind-latent',correlation_ww_lt,'wind-sensible',correlation_ww_ss

"""
fig = plt.figure(figsize=(14, 6)); ax = plt.subplot(111)
plt.xlim([0,maxx])
plt.ylabel('Bias ROMS-ECMWF [Watt/m2]', fontsize=18)
plt.plot(np.linspace(0,maxx,maxx),ssssfx[0:maxx],linewidth=2.0,  c='m', label= 'Difference in Sensible')
plt.plot(np.linspace(0,maxx,maxx),ssslfx[0:maxx],linewidth=2.0,  c='r', label= 'Difference in Latent')
plt.plot(np.linspace(0,maxx,maxx),sst[0:maxx]*10,linewidth=2.0,  c='b', label= 'Difference in SST [*10]')
plt.plot(np.linspace(0,maxx,maxx),ww[0:maxx]*5,linewidth=2.0,  c='y', label= 'Wind [*5]')
plt.xticks([b1/2,(b2-b1)/2+b1,(b3-b2)/2+b2,(maxx-b3)/2+b3],['I quarter 2004','II quarter 2004', 'III quarter 2004', 'IV quarter 2004']); 
plt.hlines(0, 0, maxx, 'm', alpha=0.7)
box = ax.get_position(); ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9]); ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=3)
plt.show()
"""
