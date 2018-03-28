from netCDF4 import Dataset
from pytides.tide import Tide
from datetime import date,datetime,timedelta
import numpy as np

lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(seconds=x)
t1=[]; A=[]; t2=[]; U=[]

def dectide(u,tt,filename):
	tide=Tide.decompose(u,tt,filename=filename)
	c = [c.name for c in tide.model['constituent']]; a = tide.model['amplitude']; p = tide.model['phase']
	return a,p,c,tide

for line in open('/media/sf_Swap-between-windows-linux/VALIDATION_GRID_NOVEMBRE_2016/Antwerpen_tides/Antwerpen_zeeschelde_2006_2007_tidal_amplitudes.prn','r').readlines()[:]:
	a = line.split( )[0][0:19]
	t1.append(datetime.strptime(a, '%Y-%m-%dT%H:%M:%S'))
	A.append(float(line.split( )[1]))

a1,p1,c1,tide1=dectide(A,t1,'Antwerpen amplitudes')

for line in open('/media/sf_Swap-between-windows-linux/VALIDATION_GRID_NOVEMBRE_2016/Antwerpen_tides/Aartselaar_2006_2007_velocities.prn','r').readlines()[:]:
	a = line.split( )[0][0:19]
	t2.append(datetime.strptime(a, '%Y-%m-%dT%H:%M:%S'))
	U.append(float(line.split( )[1]))

a2,p2,c2,tide2=dectide(U,t2,'Antwerpen velocities')
