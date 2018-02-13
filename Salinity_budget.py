from pylab import *; from netCDF4 import Dataset

def Area(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result

rr = Dataset('/scratch/ulg/mast/eivanov/NESTING10RESULTS/his_tds_long_run_10_5.nc', 'r', format='NETCDF3')# /scratch/ulg/mast/eivanov/NESTING10RESULTS/his_tds_long_run_10_nest_5.nc', 'r', format='NETCDF3')
y_vert = rr.variables['lon_rho'][:]; x_vert = rr.variables['lat_rho'][:]; Cs_w = rr.variables['Cs_w'][:]; h = rr.variables['h'][:]; mask = rr.variables['mask_rho'][:]

area=np.zeros((len(y_vert)-1,len(y_vert.T)-1)); volume=np.zeros((len(Cs_w)-1,len(y_vert),len(y_vert.T)))
for i in range(len(y_vert)-1):
	for j in range(len(x_vert.T)-1):
		poly_cartesian=[(y_vert[i,j],x_vert[i,j]),(y_vert[i,j+1],x_vert[i,j+1]),(y_vert[i+1,j+1],x_vert[i+1,j+1]),(y_vert[i+1,j],x_vert[i+1,j])]
		area[i,j]=round(Area(poly_cartesian))
		for k in range(len(Cs_w)-1):
			volume[k,i,j]=area[i,j]*h[i,j]*(Cs_w[k+1]-Cs_w[k])

salt_budget=np.zeros((len(rr.variables['ocean_time'][:]))); t = len(rr.variables['ocean_time'][:])
for p in range(t):
	a=0; b=0; s=rr.variables['salt'][p,:,:,:]
	for k in range(15):
		a=sum(np.multiply(np.matrix(ma.filled(s[k],0)),np.matrix(volume[k])))+a
		b=b+sum(volume[k])
	salt_budget[p]=a/b
	print p, salt_budget[p]

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10));
plot(rr.variables['ocean_time'][:]/60/60/24.,salt_budget)
rr.close();xlabel('Time [day]');ylabel('Salinity [psu]');fig.savefig('Salinity_parent.png', dpi=300)
