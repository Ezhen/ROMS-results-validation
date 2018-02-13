from netCDF4 import Dataset; import numpy as np; import shapely.geometry as g; import matplotlib.pyplot as plt; import matplotlib.gridspec as gridspec; import pyroms; import datetime
d = lambda x: datetime.datetime(2006,1,1,0,0,0) + datetime.timedelta(seconds=x)

g = pyroms.grid.get_ROMS_grid('COARSEST')
h = g.vgrid.h
cw= g.vgrid.Cs_w
ag=2.22; cag=np.cos(ag); sag=np.sin(ag)

def imp(var,k,x,i,j):
	vr=rr.variables[var][k,x,62+i,23+j]
	if str(type(vr))[1:6]=='class':
		vr=0
	return vr

rr = Dataset('Replotting/Transport.nc', 'r', format='NETCDF4') # Huon (112,81) Hvom (111,82)

################################################################# IMPORTANT #####################################################################
### I assume the constant shape of each grid cell as 25 km2, and an angle from northward direction as 2.22 rad for simplicity of calculations ###	2.22 radians = 127 degrees

# Dover Strait (transect number 13): 	The bridge: i = 62; j = 23,26
# [NE] North-East Direction = 145 degrees
# So, we need to turn all vectors 

### Calculation of total discharge through each grid cell for each month ###
ut=np.zeros((12,15,2,5))
vt=np.zeros((12,15,2,5))
for k in range(365*3):
	mn=int(d(rr.variables['ocean_time'][k]).month); print k # month number calculation
	for x in range(15):
		for i in range(2):
			for j in range(5):
				ut[mn-1,x,i,j]=ut[mn-1,x,i,j]+imp('Huon',k,x,i,j)
				vt[mn-1,x,i,j]=vt[mn-1,x,i,j]+imp('Hvom',k,x,i,j)
print "Calculation of total discharge through each grid cell for each month is done"

### Discharge averages calculation ###
for k in range(12):
	if k==0 or k==2 or k==4 or k==6 or k==7 or k==9:
		ut[k]=ut[k]/(31*3)
		vt[k]=vt[k]/(31*3)
	elif k==11:
		ut[k]=ut[k]/(31*3-1)
		vt[k]=vt[k]/(31*3-1)		
	elif k==3 or k==5 or k==8 or k==10:
		ut[k]=ut[k]/(30*3)
		vt[k]=vt[k]/(30*3)
	else:
		ut[k]=ut[k]/(28+28+29)
		vt[k]=vt[k]/(28+28+29)
print "Discharge averages calculation"
"""
# Recalculation of transport to rho-points northward #
ur=np.zeros((12,15,4))
vr=np.zeros((12,15,4))
for k in range(12):
	u=np.zeros((15,2,4)); v=np.zeros((15,2,5))
	for x in range(15):
		for i in range(2):
			## Turning all vector to an angle of the grid ##
			for j in range(4):
				u[x,i,j]=ut[k,x,i,j]*cag-vt[k,x,i,j]*sag
			for j in range(5):
				v[x,i,j]=ut[k,x,i,j]*sag+vt[k,x,i,j]*cag
		for m in range(4):
			print u[x,0,m], u[x,1,m]
			ur[k,x,m]=0.5*(u[x,0,m]+u[x,1,m])
			vr[k,x,m]=0.5*(v[x,0,m]+v[x,0,m+1])
	print k
print "Recalculation of transport to rho-points northward"

# Calculation of area of the grid cell #
uq=np.zeros((12,15,4))
vq=np.zeros((12,15,4))
for k in range(12):
	for x in range(15):
		for i in range(4):
			uq[k,x,i]=ur[k,x,i]*(cw[x+1]-cw[x])*h[62,23+i]*5*1000 # discharge*relative_thickness_of_water_column*total_depth_of_water_column*conversion_to_meters
			vq[k,x,i]=vr[k,x,i]*(cw[x+1]-cw[x])*h[62,23+i]*5*1000
print "Calculation of area of the grid cell"
"""
utq=np.zeros((12))
vtq=np.zeros((12))
for k in range(12):
	utq[k]=np.sum(ut[k])
	vtq[k]=np.sum(vt[k])
print "utq=",utq/(10**9), "vtq=",vtq/(10**9)
