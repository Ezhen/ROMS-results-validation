from netCDF4 import Dataset; import numpy as np; import datetime; d = lambda x: datetime.datetime(1900,1,1,0,0,0) + datetime.timedelta(hours=x); d2 = lambda x: datetime.datetime(2004,1,1,0,0,0) + datetime.timedelta(seconds=x); import matplotlib.pyplot as plt; import matplotlib as mpl; mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman')

romsvar=['sst','swrad','lwr','latent','sensible', 'evaporation', 'shflux', 'ssflux','sustr','svstr']; esmwf=['sst','ssr','str','slhf','sshf','e','ewss','nsss']

k=1; ymin,ymax,al=-2,2,0.5; b1,b2,b3=91*k,182*k,274*k; maxx=365*k; # k -scale factor

rr = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Meteo_Climatology/Meteo_2004_all_improved.nc', 'r', format='NETCDF4')
#nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/ROMS_REPLOTTED_METEO.nc', 'r', format='NETCDF4'); msk2 = nc.variables['sst'][0,:,:]
nc = Dataset('Replotting/SENSIBLE.nc', 'r', format='NETCDF4'); msk2 = nc.variables['sensible'][0,:,:]
#nc2 = Dataset('Replotting/Good_humid_all_fluxes_HIS.nc', 'r', format='NETCDF4')

sr=int((nc.variables['time'][1]-nc.variables['time'][0])/3600); srr=24/sr; se=int(rr.variables['time'][1]-rr.variables['time'][0]); ser=24/se
#ser=1;srr=1
maska=np.zeros((len(msk2),len(msk2.T))); rms=np.zeros((maxx)); r=np.zeros((maxx)); e=np.zeros((maxx));r2=np.zeros((maxx));

ff = Dataset('/media/sf_Swap-between-windows-linux/Climatology_Meteo.nc', 'r', format='NETCDF3'); msk = ff.variables['sst'][0,:,:]; 
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if type(msk[i,j]) != np.ma.core.MaskedConstant and msk2[i,j] != 0 and j>11:
			maska[i,j]=1
count=np.sum(maska); ff.close()

for i in range(len(rms)): # DAILY
	#roms_unmasked=(np.matrix(np.sum(nc.variables['swrad'][srr*i:srr*i+srr],axis=0))+np.matrix(np.sum(nc.variables['lwr'][srr*i:srr*i+srr],axis=0))+np.matrix(np.sum(nc.variables['latent'][srr*i:srr*i+srr],axis=0))+np.matrix(np.sum(nc.variables['sensible'][srr*i:srr*i+srr],axis=0))); roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count/srr
	#esmf_unmasked=(np.matrix(np.sum(rr.variables['ssr'][ser*i:ser*i+ser],axis=0))+np.matrix(np.sum(rr.variables['str'][ser*i:ser*i+ser],axis=0))+np.matrix(np.sum(rr.variables['slhf'][ser*i:ser*i+ser],axis=0))+np.matrix(np.sum(rr.variables['sshf'][ser*i:ser*i+ser],axis=0)));esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count/ser
	roms_unmasked=np.sum(nc.variables['sensible'][srr*i:srr*i+srr],axis=0)/srr; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	#roms_unmasked2=np.sum(nc2.variables['latent'][srr*i:srr*i+srr],axis=0)/srr; roms2=np.ma.masked_where(maska==0,roms_unmasked2); r2[i]=np.sum(roms2)/count
	esmf_unmasked=np.sum(rr.variables['sshf'][ser*i:ser*i+ser],axis=0)/ser;esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	rms[i]=r[i]-e[i]; print i,r[i],e[i],e[i]/r[i]
"""
for i in range(len(rms)): # SUSTR_SVSTR
	roms_unmasked=((np.sum(nc.variables['sustr'][srr*i:srr*i+srr],axis=0)/srr)**2+(np.sum(nc.variables['svstr'][srr*i:srr*i+srr],axis=0)/srr)**2)**0.5; 
	roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	esmf_unmasked=((np.sum(rr.variables['nwss'][ser*i:ser*i+ser],axis=0)/ser)**2+(np.sum(rr.variables['nsss'][ser*i:ser*i+ser],axis=0)/ser)**2)**0.5;
	esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	rms[i]=r[i]-e[i]; print i,r[i],e[i],e[i]/r[i]
"""
p=7
sssr=np.copy(r);ssse=np.copy(e);sssrms=np.copy(rms);sssr2=np.copy(rms)
for i in range(p,len(rms)-p):
	sssr[i]=sum(r[i-p:i+p])/(2*p)
	#sssr2[i]=sum(r2[i-p:i+p])/(2*p)
	ssse[i]=sum(e[i-p:i+p])/(2*p)
	sssrms[i]=sum(rms[i-p:i+p])/(2*p)
"""
for i in range(len(rms)): # INSTANTS
	roms_unmasked=nc.variables['sensible'][sr*i+sr/2]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	esmf_unmasked=rr.variables['sshf'][8*i+4]/3./3600.; esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	rms[i]=r[i]-e[i]; print i,r[i],e[i],rms[i]
"""

fig = plt.figure(figsize=(14, 6)); ax = plt.subplot(111)
plt.xlim([0,maxx]); #plt.ylim([ymin,ymax])
plt.ylabel('Bias ROMS-ECMWF [N/m2]', fontsize=18)
#plt.plot(np.linspace(0,maxx,maxx),sssrms[0:maxx],linewidth=1.0,  c='b', label= 'Difference in wind-momentum')
plt.plot(np.linspace(0,maxx,maxx),sssrms[0:maxx],linewidth=2.0,  c='b', label= 'Difference in %s' %(romsvar[4]))
plt.plot(np.linspace(0,maxx,maxx),sssr[0:maxx],linewidth=2.0, c='r', label='ROMS ')#; plt.plot(np.linspace(0,maxx,maxx),sssr2[0:maxx],'--',linewidth=1.0, c='r', label='ROMS Bulk Fluxes') 
plt.plot(np.linspace(0,maxx,maxx),ssse[0:maxx],linewidth=2.0, c='g', label='ECMWF')
plt.xticks([b1/2,(b2-b1)/2+b1,(b3-b2)/2+b2,(maxx-b3)/2+b3],['I quarter 2004','II quarter 2004', 'III quarter 2004', 'IV quarter 2004']); #yticks(linspace(-3,3,13),fontsize=16)
#plt.vlines(b1,ymin,ymax, linestyle='--', alpha=al);plt.vlines(b2,ymin,ymax, linestyle='--', alpha=al);plt.vlines(b3,ymin,ymax, linestyle='--', alpha=al)
plt.hlines(0, 0, maxx, 'm', alpha=0.7)#; plt.hlines(1, 0, 365, linestyle='--', alpha=0.7, linewidth=2.0); plt.hlines(-1, 0, 365, linestyle='--', alpha=0.7, linewidth=2.0)
box = ax.get_position(); ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9]); ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=3)
plt.show()

# INSTANT sst nc.variables['sst'][24*i+12] - sst rr.variables['sst'][4*i+2]-273.15 ; DAILYsst np.sum(nc.variables['sst'][24*i:24*i+24],axis=0)/24. - sst np.sum(rr.variables['sst'][4*i:4*i+4]-273.15,axis=0)/4. 
# DAILY swrad np.sum(nc.variables['swrad'][24*i:24*i+24],axis=0)/24. - ssr np.sum(rr.variables['ssr'][4*i:4*i+4],axis=0)/6./3600./4.
# INSTANT swrad nc.variables['swrad'][24*i+12] - ssr rr.variables['ssr'][4*i+2]/6./3600.
# INSTANT latent np.sum(nc.variables['latent'][24*i:24*i+24],axis=0)/24. - slhf np.sum(rr.variables['slhf'][8*i:8*i+8],axis=0)/3./3600./8.
# DAILY sensible nc.variables['sensible'][24*i+12] - sshf rr.variables['sshf'][8*i+4]/3./3600.
# DAILY ssflux np.sum(nc.variables['ssflux'][24*i:24*i+24],axis=0)/24. (np.sum(rr.variables['tp'][8*i:8*i+8],axis=0)+np.sum(rr.variables['e'][8*i:8*i+8],axis=0))*-800/1e7

