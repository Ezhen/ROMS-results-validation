from netCDF4 import Dataset; from tide import Tide; from datetime import date,datetime,timedelta; lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(seconds=x); import numpy as np; from scipy import spatial

MP0_lat=51+23/60.+40.04/3600.; MP0_lon=3+2./60.+44.82/3600. # MP0 (Measuring Pile 0, Oostdyckbank)
MP3_lat=51+23/60.+22.57/3600.; MP3_lon=3+11/60.+55.42/3600. # MP3 (Measuring Pile 3, Westhinder)  
MP4_lat=51+25/60.+6.08/3600. ; MP4_lon=3+17/60.+54.88/3600. # MP4 (Measuring Pile 4, Westhinder)


def dectide(u,tt,filename):
	tide=Tide.decompose(u,tt,filename=filename)
	c = [c.name for c in tide.model['constituent']]; a = tide.model['amplitude']; p = tide.model['phase']
	#a, p, c = (list(t) for t in zip(*sorted(zip(a,p,c))))
	return a,p,c, tide



rr = Dataset('/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSSNNHIS_20062008_zeta.nc', 'r', format='NETCDF3')
lats = rr.variables['lat_rho'][:]; lons = rr.variables['lon_rho'][:]; t = rr.variables['ocean_time'][:]


tt=[]
for i in range(len(t)):
	tt.append(lo(t[i]))

aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; 
idxx=spatial.KDTree(aa).query([MP0_lon,MP0_lat])[1]; idxx3=spatial.KDTree(aa).query([MP3_lon,MP3_lat])[1]; idxx4=spatial.KDTree(aa).query([MP4_lon,MP4_lat])[1]; 
k1=int(np.where(lons==aa[idxx][0])[0][0]); k2=int(np.where(lons==aa[idxx3][0])[0][0]); k3=int(np.where(lons==aa[idxx4][0])[0][0])
m1=int(np.where(lons==aa[idxx][0])[1][0]); m2=int(np.where(lons==aa[idxx3][0])[1][0]); m3=int(np.where(lons==aa[idxx4][0])[1][0])

z1 = rr.variables['zeta'][:,k1,m1]; z2 = rr.variables['zeta'][:,k2,m2]; z3 = rr.variables['zeta'][:,k3,m3]

rr.close()

az1,pz1,cz1,tidez1=dectide(z1,tt,'Residual_roms_1'); print '1'
az2,pz2,cz2,tidez2=dectide(z2,tt,'Residual_roms_2'); print '2'
az3,pz3,cz3,tidez3=dectide(z3,tt,'Residual_roms_3'); print '3'

print "M2", az1[1] ,az2[1] ,az3[1]
print "S2", az1[2] ,az2[2] ,az3[2]
print "N2", az1[3] ,az2[3] ,az3[3]
