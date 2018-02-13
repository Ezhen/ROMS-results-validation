from pylab import *; from netCDF4 import *; import gsw; import pyroms; import pyroms_toolbox

def Area(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result

rr = Dataset('/home/eivanov/COAWST/Data/ROMS/Grid/Coarsest_improved.nc', 'r', format='NETCDF3')
y_vert = rr.variables['y_vert'][:]; x_vert = rr.variables['x_vert'][:]
Cs_w = rr.variables['Cs_w'][:]; h = rr.variables['h'][:]; Cs_r = rr.variables['Cs_r'][:]
mask = rr.variables['mask_rho'][:]
rr.close()

area=np.zeros((len(y_vert)-1,len(y_vert.T)-1)); volume=np.zeros((len(Cs_w)-1,len(y_vert)-1,len(y_vert.T)-1)); Cs_array=np.zeros((len(Cs_w)-1,len(y_vert)-1,len(y_vert.T)-1));Cr_array=np.zeros((len(Cs_w)-1,len(y_vert)-1,len(y_vert.T)-1))
for i in range(len(y_vert)-1):
	for j in range(len(x_vert.T)-1):
		poly_cartesian=[(y_vert[i,j],x_vert[i,j]),(y_vert[i,j+1],x_vert[i,j+1]),(y_vert[i+1,j+1],x_vert[i+1,j+1]),(y_vert[i+1,j],x_vert[i+1,j])]
		area[i,j]=round(Area(poly_cartesian))
		for k in range(len(Cs_w)-1):
			volume[k,i,j]=area[i,j]*h[i,j]*(Cs_w[k+1]-Cs_w[k])	#volumes
			Cs_array[k,i,j]=Cs_w[k+1]-Cs_w[k]			#layer thicknesses
			Cr_array[k,i,j]=(1-(Cs_r[k]*(-1)))*h[i,j]			#relative depths
#volume=volume/10**12
print 'Volume is calculated in km3'; area_sum=sum(area); hh=tile(array(h), (15, 1))

for m in range(0,2):
	pyroms_toolbox.nc_create_roms_bdry_file('Energy_ROMS_tides_%s.nc' %(m+1), pyroms.grid.get_ROMS_grid('GRIDRECT'))
	nc = Dataset('Energy_ROMS_tides_%s.nc' %(m+1), 'a', format='NETCDF3_64BIT')
	nc.createDimension('energy_time', 364*2)
	nc.createVariable('energy_time', 'f4', ('energy_time'))
	nc.createVariable('Ek', 'f4', ('energy_time',  'eta_rho', 'xi_rho'))
	nc.createVariable('Ep', 'f4', ('energy_time',  'eta_rho', 'xi_rho'))
	nc.createVariable('EpT', 'f4', ('energy_time',  'eta_rho', 'xi_rho'))
	nc.createVariable('EpS', 'f4', ('energy_time',  'eta_rho', 'xi_rho'))
	ncdata = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/RESULTS/ocean_avg_tides%s.nc' %(m+1), 'r', format='NETCDF3')
	nc.variables['energy_time'][:]=ncdata.variables['ocean_time'][:]
	t = ncdata.variables['ocean_time'][:]
	for p in range(len(t)):
		temp=ncdata.variables['temp'][p,:,:,:]; salt=ncdata.variables['salt'][p,:,:,:]; u=ncdata.variables['u_eastward'][p,:,:,:]; v=ncdata.variables['v_northward'][p,:,:,:]
		rho_instant = gsw.rho(salt,temp,Cr_array)		
		salt_av=[sum(salt[:,i,j]*Cs_array[:,i,j]) for i in range(len(h)) for j in range(len(h.T))]
		temp_av=[sum(temp[:,i,j]*Cs_array[:,i,j]) for i in range(len(h)) for j in range(len(h.T))]
		salt_av=tile(array(salt_av).reshape(112,82), (15,1,1))
		temp_av=tile(array(temp_av).reshape(112,82), (15,1,1))
		rho_integr=gsw.rho(salt_av,temp_av,Cr_array)#; rho_integr=array(rho_integr).reshape(112,82); rho_integr = tile(array(rho_integr), (15,1,1))
		rho_T=gsw.rho(salt_av,temp,Cr_array)
		energy_instant = Cr_array*(rho_instant-rho_integr)
		energy_on_vertical=array([sum(energy_instant[:,i,j]*Cs_array[:,i,j])*9.81 for i in range(len(h)) for j in range(len(h.T))]).reshape(112,82)
		energy_instant_T = Cr_array*(rho_T-rho_integr)
		energy_on_vertical_T=array([sum(energy_instant_T[:,i,j]*Cs_array[:,i,j])*9.81 for i in range(len(h)) for j in range(len(h.T))]).reshape(112,82)			
		kin_energy_instant=(u**2+v**2)/2.
		kin_energy=array([sum(kin_energy_instant[:,i,j]*Cs_array[:,i,j]) for i in range(len(h)) for j in range(len(h.T))]).reshape(112,82)
		nc.variables['Ek'][p,:,:]=kin_energy
		nc.variables['Ep'][p,:,:]=energy_on_vertical
		nc.variables['EpT'][p,:,:]=energy_on_vertical_T
		nc.variables['EpS'][p,:,:]=energy_on_vertical-energy_on_vertical_T
		print m,p
	nc.close()

ncdata.close()

