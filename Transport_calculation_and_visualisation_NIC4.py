#! /usr/bin/env python
# -*- coding: utf-8 -*-

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import datetime
import calendar

import sys
sys.path.insert(0, '../cmocean')
import cmocean.cm as cm

d = lambda x: datetime.datetime(2006,1,1,0,0,0) + datetime.timedelta(seconds=x)

"""
Climatological discharge through the Dover strait
Ref: Salomon, Jean-Claude, Marguerite Breton, and Pierre Guegueniat. "Computed residual flow through the Dover Strait." Oceanologica acta 16.5-6 (1993): 449-455.
"""
Ref_Dover_mean = np.array([161,102,105,101,92,100,94,94,110,148,113,151,114])	# mean monthly discharge + annual
Ref_Dover_std = np.array([60,52,27,49,62,23,28,38,51,48,41,89,15.5])		# mean monthly st deviation + annual

def monthly(v):
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	"""" This function calculates monthly means for    """
	"""" residual currents across the cross-section	   """
	"""" 						   """
	"""" 		Attributes 			   """
	"""" * v - array of flows through a cross-section  """
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	v_month = np.zeros((12))
	### Discharge averages calculation ###
	for k in range(12):
		if k==0 or k==2 or k==4 or k==6 or k==7 or k==9:
			v_month[k]=v[k]/(31*3.)
		elif k==11:
			v_month[k]=v[k]/(31.*3-1)		
		elif k==3 or k==5 or k==8 or k==10:
			v_month[k]=v[k]/(30.*3)
		else:
			v_month[k]=v[k]/(28+28+29.)
		print calendar.month_name[k+1], np.int(v_month[k]), "Sv"
	return v_month

def NetCDF_read(path):
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	""" This function reads a given netCDF ROMS       """
	""" file and return several important parameters  """
	""" 					          """
	""" 		Attributes 		          """
	""" * path - path to a file                   	  """
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	rr = Dataset(path, 'r', format='NETCDF4') # Huon (112,81) Hvom (111,82) # m3 s-1
	dy = 1/rr.variables['pn'][:]
	dx = 1/rr.variables['pm'][:]
	h = rr.variables['h'][:]
	csw = rr.variables['Cs_w'][:]
	c = [csw[i+1]-csw[i] for i in range(15)]
	return rr,dy,dx,h,c
	

def Noordwijk_coef(dy,dx,h,c):
	""""""""""""""""""""""""""""""""""""""""""""""""""
	""" This function calculates relative weights  """
	""" of grid cells according to their sizes     """
	""" 					       """
	""" 		Attributes 		       """
	""" * dy - 1 / pn  (ROMS)                      """
	""" * dx - 1 / pm  (ROMS)                      """
	""" * h  - depths  (ROMS)                      """
	""" * c - relative heights of grid cells       """
	""" * yy - 1 / pn                              """
	""""""""""""""""""""""""""""""""""""""""""""""""""
	x = np.array(dx[17,24:44])[:, None] * np.outer(h[17,24:44],c) # Noordwijk 1
	y = np.array(dy[17:45,44])[:, None] * np.outer(h[17:45,44],c) # Noordwijk 2
	return x,y

def Dover_coef(dx,h,c,yy,x1,x2):
	""""""""""""""""""""""""""""""""""""""""""""""""""
	""" This function calculates relative weights  """
	""" of grid cells according to their sizes     """
	""" 					       """
	""" 		Attributes 		       """
	""" * dx - 1 / pn  (ROMS)                      """
	""" * h  - depths  (ROMS)                      """
	""" * c  - relative heights of grid cells      """
	""" * yy - transect location vertical          """
	""" * x1 - transect extent horizontal from     """
	""" * x2 - transect extent horizontal to       """
	""""""""""""""""""""""""""""""""""""""""""""""""""
	z = np.array(dx[yy,x1:x2])[:, None] * np.outer(h[yy,x1:x2],c)
	return z

def Dover_calcul(z,yy,x1,x2):
	"""""""""""""""""""""""""""""""""""""""""""""""""""""
	"""" This function calculates discharge via Dover """
	"""" 					          """
	"""" 		Attributes 		          """
	"""" * yy - transect location vertical            """
	"""" * x1 - transect extent horizontal from       """
	"""" * x2 - transect extent horizontal to         """
	""""""""""""""""""""""""""""""""""""""""""""""""""""""
	vt=np.zeros((12,15,x2-x1))
	for k in range(365*3):
		mn = int(d(rr.variables['ocean_time'][k]).month)
		vt[mn-1,:,:] += z.T * rr.variables['Hvom'][k,:,yy,x1:x2] * (-1)

	v = np.zeros((12))
	for k in range(12):
		vt[k,:,:] = vt[k,:,:] / z.T
		v[k] = np.sum(vt[k])
	v = np.around( v /(10**3), decimals=1)
	return v


def Noordwijk_calcul(x,y):
	"""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	"""" This function calculates discharge via Noordwijk """
	"""" 					              """
	"""" 		Attributes 		              """
	"""" * x - relative weihts across xi contours         """
	"""" * y - relative weihts across eta contours        """
	""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	vtn = np.zeros((12,15,48))
	for k in range(365*3):
		mn = int(d(rr.variables['ocean_time'][k]).month)
		vtn[mn-1,:,0:20] += x.T * rr.variables['Hvom'][k,:,17,24:44] * (-1)
		vtn[mn-1,:,20:]  += y.T * rr.variables['Huon'][k,:,17:45,44]

	vn = np.zeros((12))
	for k in range(12):
		vtn[k,:,0:20] = vtn[k,:,0:20] / x.T
		vtn[k,:,20:]  = vtn[k,:,20:]  / y.T
		vn[k] = np.sum(vtn[k])
	vn = np.around( vn /(10**3), decimals=1)
	return vn


if __name__ == '__main__':
	#Choose one of those: path to the file and the corresponding name of the grid, leave the others commented
	#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSSNAVG_20062008.nc'; grid = 'NN'
	path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_AVG_20062008_parent.nc'; grid = 'OW'
	#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_AVG_20062008_parent.nc'; grid = 'TW'
	#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_AVG_20062008_child.nc'; grid = 'OWc'
	#path = '/scratch/ulg/mast/eivanov/NESTING10RESULTS/NSS_TW_AVG_20062008_child.nc'; grid = 'TWc'

	rr,dy,dx,h,c = NetCDF_read(path)

	if grid == 'NN' or grid == 'OW' or grid == 'TW':
		print grid, "Noordwijk"
		x,y = Noordwijk_coef(dy,dx,h,c)
		vn  = Noordwijk_calcul(x,y)
		v_month_n = monthly(vn)
		print "Annual discharge:", int(sum(vn)/365/3.), "Sv"
		print grid, "Dover"
		z   = Dover_coef(dx,h,c,62,23,28)
		v   = Dover_calcul(z,62,23,28)
	else:
		print grid, "Dover"
		z = Dover_coef(dx,h,c,138,34,62)
		v = Dover_calcul(z,138,34,62)

	v_month = monthly(v)
	print "Annual discharge:", int(sum(v)/365/3.), "Sv"




