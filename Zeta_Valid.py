from netCDF4 import Dataset;  import numpy as np; from functions import point_inside_polygon; from iter import *; import math

def func(name,var):
	rr = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/NS_Parent_New_N_15.nc','r',format='NETCDF4') #%s_%s.nc' %(name,var),'r',format='NETCDF4')
	if name != 'OWc' and name != 'TWc':
		#nc = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/Tides_parent.nc','r',format='NETCDF4')
		nc = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Input_files_to_ROMS/Tides_Parent.nc','r',format='NETCDF4')
	else:
		nc = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/Tide_nest.nc','r',format='NETCDF4')
	msk = nc.variables['mask_rho'][:];lat=nc.variables['lat_rho'][:];lon=nc.variables['lon_rho'][:]

	const=['M2','S2','N2']
	if var == 'zeta':
		for i in range(3):
			roms_unmasked=rr.variables[const[i]][:]
			odys_unmasked=nc.variables['tide_Eamp'][i]	
			roms_mask=np.ma.masked_where(msk==0,roms_unmasked)
			odys_mask=np.ma.masked_where(msk==0,odys_unmasked)
			r = np.array([value for value in roms_mask.flatten() if not math.isnan(value)])
			o = np.array([value for value in odys_mask.flatten() if not math.isnan(value)])
			b = metrics(o,r,name,name+'_'+const[i])
			print name, const[i], 'bias', b[1], 'rms', b[2]
	elif var == 'uv':
		roms_unmasked=(rr.variables['M2_u'][:]*rr.variables['M2_u'][:]+rr.variables['M2_v'][:]*rr.variables['M2_v'][:])**0.5
		odys_unmasked=nc.variables['tide_Cmax'][0]
		roms_mask_2=np.ma.masked_where(msk==0,roms_unmasked)
		roms_mask=np.ma.masked_where(roms_mask_2>100,roms_mask_2)
		odys_mask=np.ma.masked_where(roms_mask.mask==True,odys_unmasked)
		r = np.array([value for value in roms_mask.flatten() if not math.isnan(value)])
		o = np.array([value for value in odys_mask.flatten() if not math.isnan(value)])
		b = metrics(o,r,name,name+'_'+'M2')
		print name, 'M2', 'bias', b[1], 'rms', b[2]

#nam=['NN','OW','OWc','TW','TWc']
nam= ['NN']
var = 'zeta' # 'zeta', 'uv'
for i in range(2):
	func(nam[i],var)
