from netCDF4 import Dataset; import numpy as np; import shapely.geometry as g; import matplotlib.pyplot as plt; import matplotlib.gridspec as gridspec; import pyroms; import datetime
d = lambda x: datetime.datetime(2006,1,1,0,0,0) + datetime.timedelta(seconds=x)

g = pyroms.grid.get_ROMS_grid('COARSEST')
h = g.vgrid.h
cw= g.vgrid.Cs_w
ag=2.22; cag=np.cos(ag); sag=np.sin(ag)

def imp(var,k,x,i,j):
	vr=rr.variables[var][k,x,i,j]
	return vr

rr = Dataset('Replotting/Transport.nc', 'r', format='NETCDF4') # Huon (112,81) Hvom (111,82)
"""
################################################################# IMPORTANT #####################################################################
### I assume the constant shape of each grid cell as 25 km2, and an angle from northward direction as 2.22 rad for simplicity of calculations ###	2.22 radians = 127 degrees
# Dover Strait (transect number 13): 	The bridge: i = 62; j = 23,26
### Calculation of total discharge through each grid cell for each month ###
vt=np.zeros((12,15,5))
for k in range(365*3):
	mn=int(d(rr.variables['ocean_time'][k]).month); print k # month number calculation
	for x in range(15):
		for j in range(5):
			vt[mn-1,x,j]=vt[mn-1,x,j]+imp('Hvom',k,x,62,23+j)
print "Calculation of total discharge through each grid cell for each month is done"
"""

# Noordwjik #
vt=np.zeros((12,15,48))
for k in range(365*3):
	mn=int(d(rr.variables['ocean_time'][k]).month); print k # month number calculation
	for x in range(15):
		for j in range(20):
			vt[mn-1,x,j]=vt[mn-1,x,j]+imp('Hvom',k,x,17,24+j)
		for j in range(28):
			vt[mn-1,x,20+j]=vt[mn-1,x,20+j]+imp('Huon',k,x,17+j,44)
print "Calculation of total discharge through each grid cell for each month is done"

### Discharge averages calculation ###
for k in range(12):
	if k==0 or k==2 or k==4 or k==6 or k==7 or k==9:
		vt[k]=vt[k]/(31*3)
	elif k==11:
		vt[k]=vt[k]/(31*3-1)		
	elif k==3 or k==5 or k==8 or k==10:
		vt[k]=vt[k]/(30*3)
	else:
		vt[k]=vt[k]/(28+28+29)
print "Discharge averages calculation"

vtq=np.zeros((12))
for k in range(12):
	vtq[k]=np.sum(vt[k])
print "vtq=",sum(vtq)/(10**6)/12
