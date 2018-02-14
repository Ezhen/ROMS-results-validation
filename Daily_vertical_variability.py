from netCDF4 import Dataset; import numpy as np; import matplotlib.pyplot as plt

ff = Dataset('/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSSNNHIS_1_only_meteo_temp.nc', 'r', format='NETCDF4'); msk = ff.variables['temp'][0,0,:,:]; maska=np.zeros((len(msk),len(msk.T)))
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if type(msk[i,j]) != np.ma.core.MaskedConstant:
			maska[i,j]=1
count=np.sum(maska)

k=1; ymin,ymax,al=-2,2,0.5; b1,b2,b3=91*k,182*k,274*k; maxx=365*k

av=[]; maxi=[]
for i in range(len(ff.variables['temp'][:])/24):
	roms_unmasked=np.matrix(ff.variables['temp'][i*24+15,-1,:,:])-np.matrix(ff.variables['temp'][i*24+6,-1,:,:]); roms=np.ma.masked_where(maska==0,roms_unmasked); av.append(np.sum(roms)/count); maxi.append(np.nanmax(roms))

fig = plt.figure(figsize=(12, 6)); ax = plt.subplot(111)
plt.xlim([0,maxx]); #plt.ylim([ymin,ymax])
plt.ylabel('SST difference: Day minus Night [C]', fontsize=18)
plt.plot(np.linspace(0,maxx,maxx),av,linewidth=2.0, c='g', label='Average')
plt.plot(np.linspace(0,maxx,maxx),maxi,linewidth=2.0, c='r', label='Maximum')
plt.xticks([b1/2,(b2-b1)/2+b1,(b3-b2)/2+b2,(maxx-b3)/2+b3],['I quarter 2004','II quarter 2004', 'III quarter 2004', 'IV quarter 2004']); #yticks(linspace(-3,3,13),fontsize=16)
plt.hlines(0, 0, maxx, 'm', alpha=0.7)#; plt.hlines(1, 0, 365, linestyle='--', alpha=0.7, linewidth=2.0); plt.hlines(-1, 0, 365, linestyle='--', alpha=0.7, linewidth=2.0)
box = ax.get_position(); ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9]); ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=3)
fig.savefig('SST_diff.png', dpi=200)


