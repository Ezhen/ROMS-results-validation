import numpy as np; import math; import sys,os,shutil

def aver(arr,curr,time,corr_time,limit):
	vav=0; m=0; kk=0
	for i in range(len(corr_time)):
		sys.stdout.write("Time %s is being proceeded\r" % (kk) ); sys.stdout.flush(); kk=kk+1
		if not corr_time[i]>limit:
			hour=int(time[i].split(':')[0].split("/")[2].split(" ")[1])
			try:
				vav=vav+curr[i]; m=m+1
			except:
				pass
			if i%144==0:
				try:
					arr.append(vav/m); m=0; vav=0
				except:
					arr.append('NaN'); m=0; vav=0
	return arr

def circ_aver(arr,curr,time,corr_time,limit):
	sin=0; cos=0; m=0; kk=0
	for i in range(len(corr_time)):
		sys.stdout.write("Time %s is being proceeded\r" % (kk) ); sys.stdout.flush(); kk=kk+1
		#print corr_time[i],limit
		if not corr_time[i]>limit:
			hour=int(time[i].split(':')[0].split("/")[2].split(" ")[1])
			try:
				sin=sin+np.sin(math.radians(curr[i])); cos=cos+np.cos(math.radians(curr[i])); m=m+1
			except:
				pass
			if i%144==0:
				try:
					sin=sin/m;cos=cos/m
					arr.append(math.degrees(math.atan2(sin,cos))); m=0; sin=0; cos=0
				except:
					arr.append('NaN'); m=0; sin=0; cos=0
	return arr	

def find_nearest(array,value):
	idx1 = (np.abs(array-value)).argmin()
	return array[idx1]

def appendf(dir_num,n1,n2,line):
	try:
		dir_num.append(float(line[n1:n2]))
	except:
		dir_num.append('NaN')
	return dir_num
