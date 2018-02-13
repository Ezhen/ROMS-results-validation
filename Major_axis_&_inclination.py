from netCDF4 import Dataset; import numpy as np

grid='CHILD'# 'PARENT' & 'CHILD'

if grid == 'PARENT':
	nc = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/Tides_parent.nc','r',format='NETCDF4')
elif grid == 'CHILD':
	nc = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/Tide_nest.nc','r',format='NETCDF4')
		
rr = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/AXIS_TWc.nc','r',format='NETCDF4') # AXIS_OW.nc AXIS_TW.nc AXIS_TWc.nc

msk=nc.variables['mask_rho'][:]
roms_unmasked=rr.variables['tide_Cmax'][:]; odys_unmasked=nc.variables['tide_Cmax'][0]
s=roms_unmasked-odys_unmasked
r,o=[],[]

maska=np.zeros((len(msk),len(msk.T)))
for i in range(len(msk)):
	for j in range(len(msk.T)):
		if msk[i,j] == 1 and s[i,j]<1000:
			maska[i,j]=1
			r.append(roms_unmasked[i,j])
			o.append(odys_unmasked[i,j])
count=np.sum(maska)	   


ss=np.ma.masked_where(maska==0,s);sss=np.sum(ss)/count
rms=(np.sum((np.array(r)-np.array(o))**2)/(count))**0.5
print 'Bias Major Axis:', sss
print 'RMS Major Axis:', rms
