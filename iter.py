import numpy as np; from netCDF4 import Dataset; from datetime import date, datetime, timedelta; import calendar; dt = lambda x: datetime(2006,1,1,0,0,0) + timedelta(seconds=x)	


def maskfun(msk):
	maska=np.zeros((len(msk),len(msk.T)));
	for i in range(len(msk)):
		for j in range(len(msk.T)):
			if type(msk[i,j]) != np.ma.core.MaskedConstant:
				maska[i,j]=1
	count=np.sum(maska)
	return maska, count


def metrics(o,r,name,sim):
	aa=sum((o-r)**2); bb=sum((o-np.mean(o))**2)
	#print sim, name, 'bias', round(np.mean(r-o),2), 'rms', round((np.mean((r-o)**2))**0.5,2), 'NS eff', round(1-(aa/bb),2)
	b=[sim,round(np.mean(r-o),2),round((np.mean((r-o)**2))**0.5,2),round(np.corrcoef(r,o)[0,1],2),round(1-(aa/bb),2)]
	return b


def iter1(varr,varo,rr,nc,temptype):
	rar,oar = [[] for i in range(12)],[[] for i in range(12)]
	maska, count = maskfun(rr.variables[varr][0]); maxx=1095; r=np.zeros((maxx)); o=np.zeros((maxx)); lat = rr.variables['lat'][:]; lon = rr.variables['lon'][:]
	if temptype == 'year':
		for i in range(len(r)):
			roms_unmasked=rr.variables[varr][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
			odys_unmasked=nc.variables[varo][i+731,0,31:62,44:74]; odys=np.ma.masked_where(maska==0,odys_unmasked); o[i]=np.sum(odys)/count
		return o,r
	elif temptype == 'month':
		for i in range(3*365):
			t=dt(int(rr.variables['time'][i])).month
			roms_unmasked=rr.variables[varr][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r=np.sum(roms)/count
			odys_unmasked=nc.variables[varo][i+731,0,31:62,44:74]; odys=np.ma.masked_where(maska==0,odys_unmasked); o=np.sum(odys)/count
			rar[t-1].append(r)
			oar[t-1].append(o)
		return oar,rar

def iter2(varr,varo,rr,nc,temptype):
	rar,oar = [[] for i in range(12)],[[] for i in range(12)]
	maska, count = maskfun(rr.variables[varr][0]); maxx=1095; odys_2=np.zeros((len(maska),len(maska.T))); r=np.zeros((maxx)); o=np.zeros((maxx)); lat = rr.variables['lat'][:]; lon = rr.variables['lon'][:]
	if temptype == 'year':
		for i in range(len(r)):
			roms_unmasked=rr.variables[varr][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
			odys_unmasked=nc.variables[varo][i+731,:,31:62,44:74]
			for k in range(len(odys_unmasked[0,:,0])):
				for l in range(len(odys_unmasked[0,0,:])):
					if type(rr.variables[varr][0,k,l]) != np.ma.core.MaskedConstant:
						odys_2[k,l]=odys_unmasked[np.where(odys_unmasked[:,k,l].mask==False)[0][-1],k,l]
			odys=np.ma.masked_where(maska==0,odys_2); o[i]=np.sum(odys)/count
		return o,r
	elif temptype == 'month':
		for i in range(3*365):
			t=dt(int(rr.variables['time'][i])).month
			roms_unmasked=rr.variables[varr][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
			odys_unmasked=nc.variables[varo][i+731,:,31:62,44:74]
			for k in range(len(odys_unmasked[0,:,0])):
				for l in range(len(odys_unmasked[0,0,:])):
					if type(rr.variables[varr][0,k,l]) != np.ma.core.MaskedConstant:
						odys_2[k,l]=odys_unmasked[np.where(odys_unmasked[:,k,l].mask==False)[0][-1],k,l]
			odys=np.ma.masked_where(maska==0,odys_2); o[i]=np.sum(odys)/count
			rar[t-1].append(r[i])
			oar[t-1].append(o[i])
		return oar,rar


def iter3(varr,varo,rr,nc,temptype,st):
	rar,oar = [[] for i in range(12)],[[] for i in range(12)]
	maska, count = maskfun(rr.variables[varr][0]); maxx=1095; r=np.zeros((maxx)); o=np.zeros((maxx)); lat = rr.variables['lat'][:]; lon = rr.variables['lon'][:]
	if temptype == 'year':
		for i in range(len(r)):
			roms_unmasked=rr.variables[varr][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r[i]=np.sum(roms)/count
			odys_unmasked=nc.variables[varo][i+731]; odys=np.ma.masked_where(maska==0,odys_unmasked); o[i]=np.sum(odys)/count
		return o,r
	elif temptype == 'month':
		if st=='temporal':
			for i in range(3*365):
				t=dt(int(rr.variables['time'][i])).month
				roms_unmasked=rr.variables[varr][i]; roms=np.ma.masked_where(maska==0,roms_unmasked); r=np.sum(roms)/count
				odys_unmasked=nc.variables[varo][i+731]; odys=np.ma.masked_where(maska==0,odys_unmasked); o=np.sum(odys)/count
				rar[t-1].append(r)
				oar[t-1].append(o)
			return oar,rar
		elif st=='spatial':
			for i in range(3*365):
				t=dt(int(rr.variables['time'][i])).month
				rar[t-1].append(rr.variables[varr][i].flatten())
				oar[t-1].append(nc.variables[varo][i+731].flatten())
			spar, spao = [[] for i in range(12)],[[] for i in range(12)]
			for j in range(12):
				rarj=np.array(rar[j]); oarj=np.array(oar[j])
				for k in range(len(rarj.T)):
					aa = sum(rarj[:,k])/len(rarj[:])
					bb = sum(oarj[:,k])/len(oarj[:])
					if aa>0:
						spar[j].append(aa); spao[j].append(bb)
			return spao,spar
					


def get_month_names():
	m=[]
	for i in range(12):
		m.append(calendar.month_name[i+1])
	return m
