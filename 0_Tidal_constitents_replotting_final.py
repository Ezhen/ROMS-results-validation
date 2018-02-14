from pylab import *; from netCDF4 import *

rr = Dataset('/home/eivanov/coawst_data_prrocessing/Tides_prediction/Tidal_constituents_ROMS_zeta_5_5_5.nc', 'r', format='NETCDF3')
m21 = rr.variables['M2'][:]; s21 = rr.variables['S2'][:]; n21 = rr.variables['N2'][:]
mp21 = rr.variables['MP2'][:]; sp21 = rr.variables['SP2'][:]; np21 = rr.variables['NP2'][:]
lats = rr.variables['lat'][:]; lons = rr.variables['lon'][:]
rr.close()

rr = Dataset('/home/eivanov/coawst_data_prrocessing/Tides_prediction/Tidal_constituents_ROMS_zeta_6_6_6.nc', 'r', format='NETCDF3')
m22 = rr.variables['M2'][:]; s22 = rr.variables['S2'][:]; n22 = rr.variables['N2'][:]
mp22 = rr.variables['MP2'][:]; sp22 = rr.variables['SP2'][:]; np22 = rr.variables['NP2'][:]
rr.close()

rr = Dataset('/home/eivanov/coawst_data_prrocessing/Tides_prediction/Tidal_constituents_ROMS_zeta_7_7_7.nc', 'r', format='NETCDF3')
m23 = rr.variables['M2'][:]; s23 = rr.variables['S2'][:]; n23 = rr.variables['N2'][:]
mp23 = rr.variables['MP2'][:]; sp23 = rr.variables['SP2'][:]; np23 = rr.variables['NP2'][:]
rr.close()

nc = Dataset('All_boundaries_functioning.nc', 'w', format='NETCDF3_64BIT')
nc.createDimension('eta', len(lats)); nc.createDimension('xi', len(lats.T))
nc.createVariable('lat', 'f4', ( 'eta', 'xi'))
nc.createVariable('lon', 'f4', ( 'eta', 'xi'))
nc.createVariable('M2', 'f4', ( 'eta', 'xi')); nc.createVariable('S2', 'f4', ( 'eta', 'xi')); nc.createVariable('N2', 'f4', ( 'eta', 'xi'))
nc.createVariable('MP2', 'f4', ( 'eta', 'xi')); nc.createVariable('SP2', 'f4', ( 'eta', 'xi')); nc.createVariable('NP2', 'f4', ( 'eta', 'xi'))
nc.variables['lat'][:]=lats; nc.variables['lon'][:]=lons
nc.variables['M2'][:]=m21+m22+m23; nc.variables['S2'][:]=s21+s22+s23; nc.variables['N2'][:]=n21+n22+n23; 
nc.variables['MP2'][:]=mp21+mp22+mp23; nc.variables['SP2'][:]=sp21+sp22+sp23; nc.variables['NP2'][:]=np21+np22+np23; 
"""
for i in range(len(m21)):
	for j in range(len(m21.T)):
		if m21[i,j]==m22[i,j]
			nc.variables['M2'][i,j]=m21[i,j]; nc.variables['S2'][i,j]=s21[i,j]; nc.variables['N2'][i,j]=n21[i,j]
			nc.variables['MP2'][i,j]=mp21[i,j]; nc.variables['SP2'][i,j]=sp21[i,j]; nc.variables['NP2'][i,j]=np21[i,j]
		else:
			nc.variables['M2'][i,j]=m21[i,j]+m22[i,j]; nc.variables['S2'][i,j]=s21[i,j]+s22[i,j]; nc.variables['N2'][i,j]=n21[i,j]+n22[i,j]
			nc.variables['MP2'][i,j]=mp21[i,j]+mp22[i,j]; nc.variables['SP2'][i,j]=sp21[i,j]+sp22[i,j]; nc.variables['NP2'][i,j]=np21[i,j]+np22[i,j]
"""
nc.close()

