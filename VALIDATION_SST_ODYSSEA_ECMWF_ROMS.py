from netCDF4 import Dataset;  import numpy as np; import datetime; d = lambda x: datetime.datetime(1900,1,1,0,0,0) + datetime.timedelta(hours=x); d2 = lambda x: datetime.datetime(2004,1,1,0,0,0) + datetime.timedelta(seconds=x); import matplotlib.pyplot as plt; import matplotlib as mpl; mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman'); lo = lambda x: datetime.datetime(2004,1,1,0,0,0) + datetime.timedelta(days=x)

#import matplotlib.axes.Axes.vlines as vll

k=1; ymin,ymax,al=-2,2,0.5; b1,b2,b3=91*k,182*k,274*k; maxx=365*k; # k -scale factor

#rr = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Meteo_coastline_shifted/Climatology_Meteo.nc', 'r', format='NETCDF4') #ECMWF
rr = Dataset('/media/sf_Swap-between-windows-linux/Tides/Meteo/Meteo_2004_all.nc', 'r', format='NETCDF4')
#nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/ROMS_REPLOTTED_METEO.nc', 'r', format='NETCDF4'); msk2 = nc.variables['sst'][0,:,:]
nc = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/Tide_temp.nc', 'r', format='NETCDF4'); msk2 = nc.variables['sst'][0,:,:]
nc2 = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Replotting/TEMP_GOOD_HUMIDITY.nc', 'r', format='NETCDF4')
km = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Odyssea_Replotting/analysed_sstECMWF.nc', 'r', format='NETCDF4'); msk3=km.variables['sst'][0,:,:]
fg = Dataset('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_Meteo/Boundary_temp.nc', 'r', format='NETCDF4')

maska=np.zeros((len(msk2),len(msk2.T))); r=np.zeros((maxx)); e=np.zeros((maxx)); o=np.zeros((maxx)); b=np.zeros((maxx)); y=np.zeros((maxx)); c=np.zeros((maxx)); r2=np.zeros((maxx))

ff = Dataset('/media/sf_Swap-between-windows-linux/Climatology_Meteo.nc', 'r', format='NETCDF3'); msk = ff.variables['sst'][0,:,:]; 
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if type(msk[i,j]) != np.ma.core.MaskedConstant and msk2[i,j] != 0 and j>11 and msk3[i,j]>273.15:
			maska[i,j]=1
count=np.sum(maska); ff.close()
"""
a1=fg.variables['temp_north'][0]; fg1=np.shape(a1)[0]*np.shape(a1)[1]-np.sum(a1.mask);a2=fg.variables['temp_south'][0]; fg2=np.shape(a2)[0]*np.shape(a2)[1]-np.sum(a2.mask);a3=fg.variables['temp_east'][0]; fg3=np.shape(a3)[0]*np.shape(a3)[1]-np.sum(a3.mask); fgt=fg1+fg2+fg3
for i in range(len(r)):
	b[i]=(np.sum(fg.variables['temp_north'][i])+np.sum(fg.variables['temp_south'][i])+np.sum(fg.variables['temp_east'][i]))/fgt
	y[i]=np.sum(fg.variables['temp_north'][i])/fg1; c[i]=(np.sum(fg.variables['temp_south'][i])+np.sum(fg.variables['temp_east'][i]))/(fg2+fg3)
"""
for i in range(len(r)): 
	#esmf_unmasked=-273.15+np.sum(rr.variables['sst'][8*i:8*i+8],axis=0)/4;esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	esmf_unmasked=-273.15+rr.variables['t2m'][i*8];esmf=np.ma.masked_where(maska==0,esmf_unmasked); e[i]=np.sum(esmf)/count
	###roms_unmasked=np.sum(nc.variables['sst'][24*i:24*i+24],axis=0)/24;roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	#roms_unmasked=nc.variables['sst'][i*24]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
	roms_unmasked2=nc2.variables['sst'][i*24]; roms2=np.ma.masked_where(maska==0,roms_unmasked2); r2[i]=np.sum(roms2)/count
	odys_unmasked=km.variables['sst'][i]-273.15; odys=np.ma.masked_where(maska==0,odys_unmasked); o[i]=np.sum(odys)/count

part=94
r=r=np.zeros((part))
for i in range(part): 
	roms_unmasked=nc.variables['sst'][24*i];roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count

ssse=np.copy(e); p=7
for i in range(p,len(r2*8)-p):
	ssse[i]=sum(e[i-p:i+p])/(2*p)

"""
aa=sum((o-r)**2); bb=sum((o-np.mean(o))**2)
print 'bias', np.mean(r-o), 'rms', (np.sum((r-o)**2)/(i+1))**0.5, 'nash-sutcliffe efficiency', 1-(aa/bb)
"""
fig = plt.figure(); ax = plt.subplot(111)
plt.xlim([0,maxx]); mns=min(ssse)-1; mxs=max(ssse)+1; plt.ylim([mns,mxs])
plt.ylabel('Sea Surface Temperature Night [C]', fontsize=18)
#plt.plot(np.linspace(0,maxx,maxx),r[0:maxx],linewidth=2.0, c='r', label='Good tides')
plt.plot(np.linspace(0,part,part),r[0:part],linewidth=2.0, c='r', label='Curvi_Grid')
plt.plot(np.linspace(0,maxx,maxx),r2[0:maxx],'--',linewidth=1.0,  c='r', label='ROMS Bulk Fluxes')
plt.plot(np.linspace(0,maxx,maxx),ssse[0:maxx],linewidth=1.0, c='g', label='ECMWF Air Temp')
plt.plot(np.linspace(0,maxx,maxx),o[0:maxx],linewidth=1.0, c='b', label='ODYSSEA')
#plt.plot(np.linspace(0,maxx,maxx),b[0:maxx],linewidth=1.0, c='m', label='Boundary all'); plt.plot(np.linspace(0,maxx,maxx),y[0:maxx],linewidth=1.0, c='y', label='La Manche')
#plt.plot(np.linspace(0,maxx,maxx),c[0:maxx],linewidth=1.0, c='c', label='North Sea')
#plt.xticks([b1/2,(b2-b1)/2+b1,(b3-b2)/2+b2,(maxx-b3)/2+b3],['I quarter 2004','II quarter 2004', 'III quarter 2004', 'IV quarter 2004']); #yticks(linspace(-3,3,13),fontsize=16)
plt.xticks([15*k,44*k,74*k,104*k,135*k,165*k,195*k,226*k,257*k,287*k,318*k,348*k],[lo(30).strftime("%B"),lo(58*k).strftime("%B"),lo(89*k).strftime("%B"),lo(119*k).strftime("%B"),lo(150*k).strftime("%B"),lo(180*k).strftime("%B"),lo(211*k).strftime("%B"),lo(242*k).strftime("%B"),lo(272*k).strftime("%B"),lo(303*k).strftime("%B"),lo(333*k).strftime("%B"),lo(363*k).strftime("%B")],fontsize=16)
#vll(31*k,mns,mxs, '--', alpha=0.5);vll(59*k,mns,mxs, '--', alpha=0.5);vll(90*k,mns,mxs, '--', alpha=0.5);vll(120*k,mns,mxs, '--', alpha=0.5);vll(151*k,mns,mxs, '--', alpha=0.5);vll(181*k,mns,mxs, '--', alpha=0.5);vll(212*k,mns,mxs, '--', alpha=0.5); vll(243*k,mns,mxs, '--', alpha=0.5);vll(273*k,mns,mxs, '--', alpha=0.5);vll(304*k,mns,mxs, '--', alpha=0.5);vll(334*k,mns,mxs, '--', alpha=0.5)
#plt.vlines(b1,ymin,ymax, linestyle='--', alpha=al);plt.vlines(b2,ymin,ymax, linestyle='--', alpha=al);plt.vlines(b3,ymin,ymax, linestyle='--', alpha=al)
plt.hlines(0, 0, maxx, 'm', alpha=0.7)#; plt.hlines(1, 0, 365, linestyle='--', alpha=0.7, linewidth=2.0); plt.hlines(-1, 0, 365, linestyle='--', alpha=0.7, linewidth=2.0)
box = ax.get_position(); ax.set_position([box.x0, box.y0 + box.height * 0.1,box.width, box.height * 0.9]); ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=3)
plt.show()
