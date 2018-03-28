import numpy as np; import matplotlib.pyplot as plt; from netCDF4 import Dataset; from datetime import date, datetime, timedelta; from scipy import spatial; import re; from functions import find_nearest
lo = lambda x: datetime(2006,1,1,0,0,0) + timedelta(days=x); lo2 = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)

def func_lifewatch(var):
	if var == 'temp':
		num = 29
	elif var == 'salt':
		num = 15
	stat,time,lat,lon,var,t,rt,ridx,sstR,sssR=[],[],[],[],[],[],[],[],[],[]
	for line in open('/media/sf_Swap-between-windows-linux/DATA_INPUT_ROMS/LifeWatch/Data_Vliz_Temp_Salinity','r').readlines()[1:]:
		# reading a file
		stat1 = line.split("\t")[0].split('"')[1]
		date1 = re.split('-| |:', line.split("\t")[1])
		a = line.split("\t")
		lat1,lon1,var1 = a[2],a[3],a[num]
		if int(date1[0])>2005 and int(date1[0])<2009 and var1 !='NA':
			# excluding from appending missing values and times out of the chosen simulation time frame 2006-2008
			stat.append(stat1)
			t.append(datetime(int(date1[0]),int(date1[1]),int(date1[2]),int(date1[3])))
			lat.append(float(lat1)),lon.append(float(lon1)),var.append(float(var1))

	a = np.array(list(np.unique(stat)))
	print 'unique stations:', a
	print 'unique lats:', np.array(list(np.unique(lat)))
	print 'unique lons:', np.array(list(np.unique(lon)))
	matrixx_var=np.zeros((10,12)) # 10 - number of unique stations, 12 - number of months
	count=np.zeros((10,12)); print len(var)

	for i in range(len(stat)):
		matrixx_var[np.where(stat[i]==a),t[i].month-1]=matrixx_var[np.where(stat[i]==a),t[i].month-1]+var[i]
		count[np.where(stat[i]==a),t[i].month-1]=count[np.where(stat[i]==a),t[i].month-1]+1
	for i in range(10):
		for j in range(12):
			matrixx_var[i,j]=matrixx_var[i,j]/count[i,j]

	return matrixx_var

