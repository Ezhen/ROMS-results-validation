from pylab import *; from netCDF4 import *; import datetime; import matplotlib as mpl

lo = lambda x: datetime.datetime(2013,1,1,0,0,0) + datetime.timedelta(days=x)
mpl.rcParams['axes.unicode_minus']=False

mpl.rc('font',family='Times New Roman')


def Area(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result

nc = Dataset('Energy_ROMS_1.nc', 'r', format='NETCDF3_64BIT')
ep = nc.variables['Ep'][:]						# Ek - kinetic; Ep - potential
ept = nc.variables['EpT'][:]
eps = nc.variables['EpS'][:]
nc.close()

rr = Dataset('/home/eivanov/COAWST/Data/ROMS/Grid/Coarsest_improved.nc', 'r', format='NETCDF3')
y_vert = rr.variables['y_vert'][:]; x_vert = rr.variables['x_vert'][:]; msk = rr.variables['mask_rho'][:]
rr.close()

area=np.zeros((len(y_vert)-1,len(y_vert.T)-1))
for i in range(len(y_vert)-1):
	for j in range(len(x_vert.T)-1):
		poly_cartesian=[(y_vert[i,j],x_vert[i,j]),(y_vert[i,j+1],x_vert[i,j+1]),(y_vert[i+1,j+1],x_vert[i+1,j+1]),(y_vert[i+1,j],x_vert[i+1,j])]
		area[i,j]=round(Area(poly_cartesian))

ar=sum(area[msk==1])
ep[isnan(ep)]=0
ep1=[sum(ep[p]*area)/ar for p in range(len(ep))]

ept[isnan(ept)]=0
ept1=[sum(ept[p]*area)/ar for p in range(len(ept))]

eps[isnan(eps)]=0
eps1=[sum(eps[p]*area)/ar for p in range(len(eps))]

xlim(0,364); ylim(min(ep1),max(ept1))
plot(ep1, label='Total anomaly',linewidth=2)
plot(ept1, label='Anomaly due to temperature',linewidth=2)
plot(eps1, label='Anomaly due to salinity',linewidth=2)
xticks([15,44,74,104,135,165,195,226,257,287,318,348],[lo(30).strftime("%B"),lo(58).strftime("%B"),lo(89).strftime("%B"),lo(119).strftime("%B"),lo(150).strftime("%B"),lo(180).strftime("%B"),lo(211).strftime("%B"),lo(242).strftime("%B"),lo(272).strftime("%B"),lo(303).strftime("%B"),lo(333).strftime("%B"),lo(363).strftime("%B")], fontsize=16)
vlines(31,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(59,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(90,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(120,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(151,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(181,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(212,min(ep1),max(ept1), linestyle='--', alpha=0.5); vlines(243,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(273,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(304,min(ep1),max(ept1), linestyle='--', alpha=0.5);vlines(334,min(ep1),max(ept1), linestyle='--', alpha=0.5)
hlines(0, 1, 364,  alpha=0.5,linestyle='--');hlines(-5, 1, 364, alpha=0.5,linestyle='--');hlines(-10, 1, 364, alpha=0.5,linestyle='--');hlines(-15, 1, 364,  alpha=0.5,linestyle='--')
legend(loc=3)
show()


