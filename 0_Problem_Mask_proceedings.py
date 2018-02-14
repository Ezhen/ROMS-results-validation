import numpy as np; import matplotlib.pyplot as plt; import matplotlib as mpl; import re; from datetime import date, datetime, timedelta; from netCDF4 import Dataset;from scipy import spatial
mpl.rcParams['axes.unicode_minus']=False; mpl.rc('font',family='Times New Roman'); lo = lambda x: datetime(2004,1,1,0,0,0) + timedelta(days=x); lo2 = lambda x: datetime(2004,1,1,0,0,0) + timedelta(seconds=x)

#ncdata1 = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/Interannual_results/his.nc', 'r', format='NETCDF3') # Non-tidal
ncdata1 = Dataset('/media/sf_Swap-between-windows-linux/Grid_Nesting/RESULTS/his_tds_long_run_10_5_nonest_try_temp_salt_u_v_level_13_time_subset.nc', 'r', format='NETCDF3') # Tidal 
lats = ncdata1.variables['lat_rho'][:]; lons = ncdata1.variables['lon_rho'][:]; times = ncdata1.variables['ocean_time'][:]; #hs = ncdata1.variables['h'][:]#; Cs = ncdata1.variables['Cs_r'][:]

def find_nearest(array,value):
	idx1 = (np.abs(array-value)).argmin(); #print t[i]*24*60*60, array[idx]
	array2=array.copy();array2[idx1]=-999
	idx2 = (np.abs(array2-value)).argmin()
	return array[idx1], array[idx2]

def read(array, number):
	for line in open('Data_Vliz_Temp_Salinity','r').readlines()[1:]:
		if array==stat:
			array.append(line.split("\t")[number].split('"')[1])
		elif array==time:
			array.append(re.split('-| |:', line.split("\t")[number]))
		else:
			try:
				array.append(float(line.split("\t")[number]))
			except:
				array.append('NaN')

stat=[]; time=[]; lat=[]; lon=[]; pres=[]; salt=[]; temp=[]; t=[]
read(stat,0); read(time,1); read(lat,2); read(lon,3); read(salt,15); read(pres,19); read(temp,29)

for i in range(len(time)):
	try:
		t.append((date(int(time[i][0]),int(time[i][1]),int(time[i][2]))-date(2004,1,1)).days+int(time[i][3])/24.)
		#print time[i], lo(t[-1])
	except:
		t.append(time[i])

stat1=[]; time1=[]; lat1=[]; lon1=[]; pres1=[]; salt1=[]; temp1=[]; stat11=3; diff_temp=[]; diff_salt=[]; tempvliz=[]; saltvliz=[]
for i in range(len(time)):
	if float(time[i][0])<2004 or float(time[i][0])>2004:#>2013:
		pass #time1.append('NaN')
	else:
		time1.append(find_nearest(times,t[i]*24*60*60)[0]/24/60/60.)
		if stat[i] == stat11:
			lon1.append(lon1[-1]); lat1.append(lat1[-1])#; pres1.append(round(pres1[-1],1))
		else:
			aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; idxx=spatial.KDTree(aa).query([lon[i],lat[i]])[1]
			lon1.append(aa[idxx][0]); lat1.append(aa[idxx][1])
			#pres1.append(hs.flatten()[idxx])
			stat11=stat[i]
		maximum, minimum=max(find_nearest(times,t[i]*24*60*60)[0],find_nearest(times,t[i]*24*60*60)[1]),min(find_nearest(times,t[i]*24*60*60)[0],find_nearest(times,t[i]*24*60*60)[1])
		rel=(abs(lo2(maximum).hour-(int(time[i][3])+int(time[i][4])/60.)))/6.
		#temp_0=np.zeros((len(lats),len(lats.T)));temp_1=np.zeros((len(lats),len(lats.T)))
		temp_0=ncdata1.variables['temp'][int(np.where(times==minimum)[0][0]),0,int(np.where(lons==lon1[-1])[0][0]),int(np.where(lons==lon1[-1])[1][0])]
		temp_1=ncdata1.variables['temp'][int(np.where(times==maximum)[0][0]),0,int(np.where(lons==lon1[-1])[0][0]),int(np.where(lons==lon1[-1])[1][0])]
		temp1.append(temp_0*rel+temp_1*(1.-rel))
		salt1.append(ncdata1.variables['salt'][int(np.where(times==find_nearest(times,t[i]*24*60*60)[0])[0][0]),0,int(np.where(lons==lon1[-1])[0][0]),int(np.where(lons==lon1[-1])[1][0])])
		print i, time[i], lo2(find_nearest(times,t[i]*24*60*60)[0]), lons[int(np.where(lons==lon1[-1])[0][0]),int(np.where(lons==lon1[-1])[1][0])], lon[i], lats[int(np.where(lons==lon1[-1])[0][0]),int(np.where(lons==lon1[-1])[1][0])], lat[i], salt[i], salt1[-1]#,temp[i], temp1[-1], temp_0, temp_1 
		#hvliz.append(ncdata1.variables['h'][int(np.where(lons==lon1[-1])[0][0]),int(np.where(lons==lon1[-1])[1][0])])
		tempvliz.append(temp[i]); saltvliz.append(salt[i])
		stat1.append(stat[i])
		if temp[i] != 'NaN':
			diff_temp.append(round(temp[i]-temp1[-1],2))
		else:
			diff_temp.append('NaN')
		if salt[i] != 'NaN':
			diff_salt.append(round(salt[i]-salt1[-1],2))
		else:
			diff_salt.append('NaN')
		#print i, 'station:', stat1[-1], 'temperature:', diff_temp[-1], 'salinity:', diff_salt[-1]
ncdata1.close()

##########################
###### Bad script ########
##########################
"""
# VLIZ ROMS comparison stations
fig=plt.figure(figsize=(12, 12))
for j in range(len(list(set(stat)))):
	b=np.where(np.array(stat)==list(set(stat))[j])
	plt.scatter(tempvliz[b[0][0]:b[0][-1]],temp1[b[0][0]:b[0][-1]], c=mpl.cm.rainbow(255*j/len(list(set(stat)))), s=50, label=list(set(stat))[j], edgecolors='black')
	plt.xticks(np.linspace(0,25,6),fontsize=20)
	plt.yticks(np.linspace(0,25,6),fontsize=18); plt.ylabel('Temperature ROMS', fontsize=20); plt.xlabel('Temperature VLIZ', fontsize=20)
	plt.legend(loc=1,ncol=8,title='Abs temperature VLIZ / ROMS',prop={'size':12}); plt.plot([0,25], [0,25], ls="--", c=".3"); plt.xlim(0,25); plt.ylim(0,25)
fig.savefig('VLIZ_ROMS_relation_stations', dpi=200)#; plt.show()

# VLIZ ROMS comparison stations
fig=plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111)
for j in range(len(list(set(stat)))):
	b=np.where(np.array(stat)==list(set(stat))[j])
	plt.scatter(tempvliz[b[0][0]:b[0][-1]],temp1[b[0][0]:b[0][-1]], c=mpl.cm.rainbow(1.0-round(float(list(set(pres1))[j]-min(list(set(pres1))))/(max(list(set(pres1)))-min(list(set(pres1)))),1)), s=50, label=round(list(set(pres1))[j],2), edgecolors='black')
	plt.xticks(np.linspace(0,25,6),fontsize=18)
	plt.yticks(np.linspace(0,25,6),fontsize=18); plt.ylabel('Temperature ROMS', fontsize=20); plt.xlabel('Temperature VLIZ', fontsize=20)
	handles, labels = ax.get_legend_handles_labels(); labels, handles = zip(*sorted(zip(map(float, labels), handles)))
	ax.legend(handles, labels, ncol=8, title='Absolute temperature VLIZ / ROMS',prop={'size':12})
	plt.plot([0,25], [0,25], ls="--", c=".3"); plt.xlim(0,25); plt.ylim(0,25)#; plt.show()
fig.savefig('VLIZ_ROMS_relation_bathymetry', dpi=200)
"""
"""
for j in range(len(list(set(stat)))):
	b=np.where(np.array(stat)==list(set(stat))[j])
	plt.scatter(t[b[0][0]:b[0][-1]],temp[b[0][0]:b[0][-1]], c=mpl.cm.rainbow(255*j/len(list(set(stat)))), s=50, label=list(set(stat))[j], edgecolors='black',marker='o')
	plt.scatter(time1[b[0][0]:b[0][-1]],temp1[b[0][0]:b[0][-1]], c=mpl.cm.rainbow(255*j/len(list(set(stat)))), s=50, label=list(set(stat))[j], edgecolors='black',marker='>')
	plt.xticks([-730,-365,0,366,731,1096,1462,1827,2192,2557,2923,3288,3653,4018,4384],[lo(-730).strftime("%Y"),lo(-365).strftime("%Y"),lo(0).strftime("%Y"),lo(366).strftime("%Y"),lo(731).strftime("%Y"),lo(1096).strftime("%Y"),lo(1462).strftime("%Y"),lo(1827).strftime("%Y"),lo(2192).strftime("%Y"),lo(2557).strftime("%Y"),lo(2923).strftime("%Y"),lo(3288).strftime("%Y"),lo(3654).strftime("%Y"),lo(4018).strftime("%Y"),lo(4384).strftime("%Y")],fontsize=18)
	plt.yticks(fontsize=18); plt.ylabel('Temperature [C]', fontsize=20); plt.xlabel('Time [year]', fontsize=20)
	plt.legend(loc=1,ncol=8,title='VLIZ Stations (circles) and ROMS (triangels)',prop={'size':12})
	#plt.xlim(950,990)
plt.show()
"""



moins_temp = [[] for i in range(12)]; moins_salt = [[] for i in range(12)]
for m in range(len(stat1)):
	if diff_temp[m] != 'NaN':
		moins_temp[int(lo(time1[m]).month)-1].append(diff_temp[m])
	if diff_salt[m] != 'NaN':
		moins_salt[int(lo(time1[m]).month)-1].append(diff_salt[m])
moins_temp_avg=np.zeros((12)); moins_salt_avg=np.zeros((12))
for m in range(12):
	try:
		moins_temp_avg[m]=sum(moins_temp[m])/len(moins_temp[m]); moins_salt_avg[m]=sum(moins_salt[m])/len(moins_salt[m])
	except:
		moins_temp_avg[m]='NaN'
# Temperature temporal
fig=plt.figure(figsize=(20, 12))#; plt.suptitle(var[m],family='Courier New, monospace',fontsize=20, y=0.88)
plt.scatter(-0.5+np.ones((len(moins_temp[0]))),np.array(moins_temp[0]), label='Observed VLIZ value minus corresponding ROMS value')
for i in range(1,12):
	plt.scatter(0.5+i*np.ones((len(moins_temp[i]))),np.array(moins_temp[i]))
plt.plot(np.arange(0.5,12.5),moins_temp_avg, 'r', linewidth=3, label='Mean difference in temperature: VLIZ minus ROMS')
plt.xticks(np.arange(0.5,12.5),["January","Febraury","March","April","May","June","July","August","September","October","November","December"],fontsize=16)
plt.xlim(0,12); plt.ylim(-10,10); plt.ylabel('Temperature difference [C]', fontsize=20); plt.xlabel('Month', fontsize=20); plt.legend(loc=1,prop={'size':18}); plt.hlines(0, 0, 12, linestyle='--', alpha=0.7, linewidth=1.0); plt.yticks(np.linspace(-10,10,21),fontsize=16)#; plt.show()
fig.savefig('Temperature_temporal', dpi=200); print 'Figure Temperature_temporal is saved'

# Salinity temporal
fig=plt.figure(figsize=(20, 12))#; plt.suptitle(var[m],family='Courier New, monospace',fontsize=20, y=0.88)
plt.scatter(-0.5+np.ones((len(moins_salt[0]))),np.array(moins_salt[0]), label='Observed VLIZ value minus corresponding ROMS value')
for i in range(1,12):
	plt.scatter(0.5+i*np.ones((len(moins_salt[i]))),np.array(moins_salt[i]))
plt.plot(np.arange(0.5,12.5),moins_salt_avg, 'r', linewidth=3, label='Mean difference in salinity: VLIZ minus ROMS')
plt.xticks(np.arange(0.5,12.5),["January","Febraury","March","April","May","June","July","August","September","October","November","December"],fontsize=16)
plt.xlim(0,12); plt.ylim(-8,8); plt.ylabel('Salinity difference [PSU]', fontsize=20); plt.xlabel('Month', fontsize=20); plt.legend(loc=1,prop={'size':18}); plt.hlines(0, 0, 12, linestyle='--', alpha=0.7, linewidth=1.0); plt.yticks(np.linspace(-8,8,17),fontsize=16)#; plt.show()
fig.savefig('Salinity_temporal', dpi=200); print 'Figure Salinity_temporal is saved'


ustat=set(stat1); spat_temp = [[] for i in range(len(ustat))]; spat_salt = [[] for i in range(len(ustat))]
for m in range(len(stat1)):
	if diff_temp[m] != 'NaN':
		spat_temp[int(np.where(np.array(list(ustat))==stat1[m])[0][0])].append(diff_temp[m])
	if diff_salt[m] != 'NaN':
		spat_salt[int(np.where(np.array(list(ustat))==stat1[m])[0][0])].append(diff_salt[m])
		if stat1[m]=='710':
			print diff_salt[m]
spat_temp_avg=np.zeros((len(ustat))); spat_salt_avg=np.zeros((len(ustat)))
for m in range(len(ustat)):
	try:
		spat_temp_avg[m]=sum(spat_temp[m])/len(spat_temp[m]); spat_salt_avg[m]=sum(spat_salt[m])/len(spat_salt[m])
	except:
		spat_temp_avg[m]='NaN'; spat_salt_avg[m]='NaN'

# Temperature spatial
fig=plt.figure(figsize=(20, 12))
try:
	plt.scatter(-0.5+np.ones((len(spat_temp[0]))),np.array(spat_temp[0]),color='b', label='Observed VLIZ value minus corresponding ROMS value')
except:
	pass
for i in range(1,len(ustat)):
	try:
		plt.scatter(0.5+i*np.ones((len(spat_temp[i]))),np.array(spat_temp[i]), color='b')
	except:
		pass
plt.scatter(np.arange(0.5,10.5),spat_temp_avg, color='r', s=100, label='Mean difference in temperature: VLIZ minus ROMS')
plt.xticks(np.arange(0.5,10.5),list(ustat),fontsize=20)
plt.xlim(0,10); plt.ylim(-10,10); plt.ylabel('Temperature difference [C]', fontsize=20); plt.xlabel('Station', fontsize=20); plt.legend(loc=1,prop={'size':18}); plt.hlines(0, 0, 16, linestyle='--', alpha=0.7, linewidth=1.0); plt.yticks(np.linspace(-10,10,21),fontsize=16)#; plt.show()
fig.savefig('Temperature_spatial', dpi=200); print 'Figure Temperature_spatial is saved'

# Salinity spatial
fig=plt.figure(figsize=(20, 12))
try:
	plt.scatter(-0.5+np.ones((len(spat_salt[0]))),np.array(spat_salt[0]),color='b', label='Observed VLIZ value minus corresponding ROMS value')
except:
	pass
for i in range(1,len(ustat)):
	try:
		plt.scatter(0.5+i*np.ones((len(spat_salt[i]))),np.array(spat_salt[i]), color='b')
	except:
		pass
plt.scatter(np.arange(0.5,10.5),spat_salt_avg, color='r', s=100, label='Mean difference in salinity: VLIZ minus ROMS')
plt.xticks(np.arange(0.5,10.5),list(ustat),fontsize=20)
plt.xlim(0,10); plt.ylim(-8,8); plt.ylabel('Salinity difference [PSU]', fontsize=20); plt.xlabel('Station', fontsize=20); plt.legend(loc=1,prop={'size':18}); plt.hlines(0, 0, 16, linestyle='--', alpha=0.7, linewidth=1.0); plt.yticks(np.linspace(-8,8,17),fontsize=16)#; plt.show()
fig.savefig('Salinity_spatial', dpi=200); print 'Figure Salinity_spatial is saved'


