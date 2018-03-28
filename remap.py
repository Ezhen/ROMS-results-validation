from netCDF4 import Dataset; import numpy as np; from numpy import shape; import pyroms; import pyroms_toolbox; from datetime import datetime

def remap(tt,  src_file, src_varname, wts, src_grd, dst_grd, src_grd_file,order,grid):
	wts_file = wts;  spval= -32767
	cdf = Dataset(src_file); 
	Mp,Np = dst_grd.lon_t.shape; 
	src_var = cdf.variables[src_varname][:]
	dst_file = src_varname + dst_grd.name + '.nc'
	time=cdf.variables['ocean_time'][0:tt]
	if src_varname=='sst':
		nc1 = Dataset(src_grd_file, 'r', format='NETCDF4'); lat1=nc1.variables['lat'][:]; lon1=nc1.variables['lon'][:]; nc1.close()
	else:
		nc1 = Dataset(src_grd_file, 'r', format='NETCDF4'); lon1 = nc1.variables['lon'][22:93]; lat1 = nc1.variables['lat'][18:86]; nc1.close()
	nc = Dataset(dst_file, 'w', format='NETCDF4')
	nc.createDimension('lat', len(lat1)); nc.createDimension('lon', len(lon1))
	nc.createDimension('time', tt); nc.createVariable('time', 'f4', 'time'); nc.createVariable('lat', 'f4', 'lat'); nc.createVariable('lon', 'f4', 'lon')
	nc.variables['time'].long_name = 'time'; nc.variables['time'].units = 'days since 2006-01-01 00:00:00'; nc.variables['time'].field = 'time field'; nc.variables['time'][:] = time
	nc.variables['lat'][:] = lat1; nc.variables['lon'][:] = lon1
	dimensions = ('time', 'lat', 'lon'); Bpos = 't'; Cpos = 'rho'
	if src_varname=='sst':
		dst_varname = 'sst'; long_name = 'sea surface temperature'; units = 'Celsius'; field = 'sst, scalar, series'
	if src_varname=='sbt':
		dst_varname = 'sbt'; long_name = 'sea bottom temperature'; units = 'Celsius'; field = 'sbt, scalar, series'
	if src_varname=='sss':
		dst_varname = 'sss'; long_name = 'sea surface salinity'; units = 'Psu'; field = 'sss, scalar, series'
	if src_varname=='sbs':
		dst_varname = 'sbs'; long_name = 'sea bottom salinity'; units = 'Psu'; field = 'sbs, scalar, series'
	if src_varname=='ssu':
		dst_varname = 'ssu'; long_name = 'u-eastward surface velocity'; units = 'm*s-1'; field = 'ssu, scalar, series'
	if src_varname=='ssv':
		dst_varname = 'ssv'; long_name = 'v-northward surface velocity'; units = 'm*s-1'; field = 'ssv, scalar, series'
	if src_varname=='sbu':
		dst_varname = 'sbu'; long_name = 'u-eastward bottom velocity'; units = 'm*s-1'; field = 'sbu, scalar, series'
	if src_varname=='sbv':
		dst_varname = 'sbv'; long_name = 'v-northward bottom velocity'; units = 'm*s-1'; field = 'sbv, scalar, series'
	nc.createVariable(dst_varname, 'f8', dimensions, fill_value=spval)
	nc.variables[dst_varname].long_name = long_name; nc.variables[dst_varname].units = units; nc.variables[dst_varname].field = field; dst_var=np.zeros((tt, Mp,Np))  	
	for i in range(len(time)):
		src_varz = cdf.variables[src_varname][i,:,:]
		dst_cont = pyroms.remapping.remap(src_varz, wts_file, spval=spval)#; print np.shape(nc.variables[dst_varname][i]),np.shape(np.ma.masked_where(dst_grd.mask_t==0,dst_cont))
		nc.variables[dst_varname][i]=np.ma.masked_where(dst_grd.mask_t==0,dst_cont)#; print i; print dst_grd.mask_t
	print src_varname, dst_varname, 'is written into the separated netcdf file'
	nc.close()
