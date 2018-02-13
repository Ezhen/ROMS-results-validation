from netCDF4 import Dataset;  import numpy as np; from texttable import Texttable; from iter import *; from plotfunc import *; import calendar

def mainfunc(sim,grid,a,temptype,st):
	if a=='sst':
		rr = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/%s_sstODYSSEA_%s.nc' %(sim,grid),'r',format='NETCDF4') 
		nc = Dataset('/home/eivanov/coawst_data_prrocessing/Validation_FTP_Nested.nc', 'r', format='NETCDF4'); b=[]
		if temptype=='year':
			o,r = iter3('sst','sst',rr,nc,temptype,st); o = o-273.15; b = metrics(o,r,'SST',sim)
		elif temptype=='month':
			o,r = iter3('sst','sst',rr,nc,temptype,st)
			for i in range(12):
				b.append(metrics(np.array(o[i])-273.15,np.array(r[i]),'SST',calendar.month_name[i+1]))
	else:
		rr = Dataset('/home/eivanov/coawst_data_prrocessing/VALIDATION/Replotting/%s_replottedMERCATOR_%s.nc' %(sim,grid),'r',format='NETCDF4') 
		nc = Dataset('/media/sf_Swap-between-windows-linux/New_Grid/TEMP_SALT_CURR_2004_2014.nc', 'r', format='NETCDF4'); b=[]
		if a=='salt':
			if temptype=='year':
				o,r = iter1('salt','vosaline',rr,nc,temptype); b = metrics(o,r,'SSS',sim)
			elif temptype=='month':
				o,r = iter1('salt','vosaline',rr,nc,temptype)
				for i in range(12):
					b.append(metrics(np.array(o[i]),np.array(r[i]),'SSS',calendar.month_name[i+1]))
		elif a=='sbt':
			if temptype=='year':
				o,r = iter2('sbt','votemper',rr,nc,temptype); o = o-273.15; b = metrics(o,r,'TBT',sim)
			elif temptype=='month':
				o,r = iter2('sbt','votemper',rr,nc,temptype);
				for i in range(12):
					b.append(metrics(np.array(o[i])-273.15,np.array(r[i]),'TBT',calendar.month_name[i+1]))
		#elif a=='ssu':
		#	o,r = iter1('ssu','vozocrtx',rr,nc,temptype); b = metrics(o,r,'Surface U-velocity',sim)
		#elif a=='ssv':
		#	o,r = iter1('ssv','vomecrty',rr,nc,temptype); b = metrics(o,r,'Surface V-velocity',sim)
		#elif a=='sbu':
		#	o,r = iter2('sbu','vozocrtx',rr,nc,temptype); b = metrics(o,r,'Bottom U-velocity',sim)
		#elif a=='sbv':
		#	o,r = iter2('sbv','vomecrty',rr,nc,temptype); b = metrics(o,r,'Bottom V-velocity',sim)
		else:
			print 'no variables are found'
	rr.close(); nc.close()
	return o,r,b


simi = ['NN_bulk','OW_bulk','TW_bulk','OWc_bulk','TWc_bulk']
#simi = ['NN','OW','TW','OWc','TWc']
gridi = ['PARENT','PARENT','PARENT','NEST','NEST']
nameg = ['No Nest','One Way Parent','Two Way Parent','One Way Child','Two Way Child']; monthname=get_month_names()
#vari = ['sst','salt','sbt']#,'ssu','ssv','sbu','sbv']
vari = ['sst']
month = np.arange(12)+1
temptype='month' # 'year', 'month'
dop= 'no_need' # 'need_temporal','no_need'
st='spatial' #'spatial','temporal'
for j in range(len(vari)):
	var = vari[j]
	olist,rlist,bb = [],[],[]
	if temptype == 'month':
		for n in range(5):
			o,r,b = mainfunc(simi[n],gridi[n],var,temptype,st)
			t = Texttable(); t.add_rows([[simi[n]+': '+var, 'Bias','RMS','Corr','NS Coef'],b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11]]); print t.draw()
			varr=var+'_'+simi[n]
			#plotfunc(o,r,monthname,varr,dop,temptype)
	elif temptype == 'year':
		for n in range(5):
			o,r,b = mainfunc(simi[n],gridi[n],var,temptype,st)
			olist.append(o)
			rlist.append(r)
			bb.append(b)
		t = Texttable(); t.add_rows([['Year: '+var, 'Bias','RMS','Corr','NS Coef'],bb[0],bb[1],bb[2],bb[3],bb[4]]); print t.draw(); plotfunc(olist,rlist,nameg,var,dop,temptype)
