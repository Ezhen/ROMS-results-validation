from netCDF4 import Dataset

name='/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_HIS_20062008_parent.nc'
dst='TW.nc'

nc = Dataset(name, 'r', format='NETCDF4')

rr = Dataset(dst, 'w', format='NETCDF4')
rr.createDimension('time', len(nc.variables['temp'][:,0,0,0])/24)
rr.createDimension('eta_rho', len(nc.variables['temp'][0,0,:,0]))
rr.createDimension('xi_rho', len(nc.variables['temp'][0,0,0,:]))

rr.createVariable('time', 'f4', ('time'))
rr.createVariable('lat_rho', 'f4', ('eta_rho','xi_rho'))
rr.createVariable('lon_rho', 'f4', ('eta_rho','xi_rho'))
rr.createVariable('mask_rho', 'f4', ('eta_rho','xi_rho'))
rr.createVariable('h', 'f4', ('eta_rho','xi_rho'))
rr.variables['lat_rho'][:]=nc.variables['lat_rho'][:]
rr.variables['lon_rho'][:]=nc.variables['lon_rho'][:]
rr.variables['mask_rho'][:]=nc.variables['mask_rho'][:]
rr.variables['h'][:]=nc.variables['h'][:]

rr.createVariable('sst', 'f4', ('time','eta_rho','xi_rho'))
rr.createVariable('sss', 'f4', ('time','eta_rho','xi_rho'))
rr.createVariable('tbt', 'f4', ('time','eta_rho','xi_rho'))
for i in range(len(nc.variables['ocean_time'][:])):
	if i%24==0:
		rr.variables['time'][i/24]=nc.variables['ocean_time'][i]
		rr.variables['sst'][i/24]=nc.variables['temp'][i,13,:,:]
		rr.variables['sss'][i/24]=nc.variables['salt'][i,13,:,:]
		rr.variables['tbt'][i/24]=nc.variables['temp'][i,0,:,:]
		print i
		

rr.close()
nc.close()
