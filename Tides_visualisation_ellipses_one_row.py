from pylab import *; import matplotlib.gridspec as gridspec; from netCDF4 import Dataset; from scipy import spatial; from functions import *
plt.rcParams["font.family"] = 'Times New Roman'; mpl.rcParams['axes.unicode_minus']=False

MP0_lat=51+23/60.+40.04/3600.; MP0_lon=3+2./60.+44.82/3600. # MP0 (Measuring Pile 0, Oostdyckbank)
MP3_lat=51+23/60.+22.57/3600.; MP3_lon=3+11/60.+55.42/3600. # MP3 (Measuring Pile 3, Westhinder)  
MP4_lat=51+25/60.+6.08/3600. ; MP4_lon=3+17/60.+54.88/3600. # MP4 (Measuring Pile 4, Westhinder)

u = [0.6, 0.761, 0.709]
up = [3.16, 358.78, 338.09]
v = [0.244, 0.22, 0.147]
vp = [54.61, 35.2, 80.14]
vliz=['MP0','MP3','MP4']

name = 'OWc'

ticks=list(np.array(range(0,11))/5.-1)
def func(name):
	nc = Dataset('Replotting/%s_uv.nc' %(name), 'r', format='NETCDF4')
	lats = nc.variables['lat'][:]; lons = nc.variables['lon'][:]
	aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; 
	idxx=spatial.KDTree(aa).query([MP0_lon,MP0_lat])[1]; idxx3=spatial.KDTree(aa).query([MP3_lon,MP3_lat])[1]; idxx4=spatial.KDTree(aa).query([MP4_lon,MP4_lat])[1]; 
	k1=int(np.where(lons==aa[idxx][0])[0][0]); k2=int(np.where(lons==aa[idxx3][0])[0][0]); k3=int(np.where(lons==aa[idxx4][0])[0][0])
	l1=int(np.where(lons==aa[idxx][0])[1][0]); l2=int(np.where(lons==aa[idxx3][0])[1][0]); l3=int(np.where(lons==aa[idxx4][0])[1][0])
	nc = Dataset('Replotting/%s_uv.nc' %(name), 'r', format='NETCDF4')
	uu = [nc.variables['M2_u'][k1,l1],nc.variables['M2_u'][k2,l2],nc.variables['M2_u'][k3,l3]]
	vv = [nc.variables['M2_v'][k1,l1],nc.variables['M2_v'][k2,l2],nc.variables['M2_v'][k3,l3]]
	rup = [nc.variables['MP2_u'][k1,l1],nc.variables['MP2_u'][k2,l2],nc.variables['MP2_u'][k3,l3]]
	rvp = [nc.variables['MP2_v'][k1,l1],nc.variables['MP2_v'][k2,l2],nc.variables['MP2_v'][k3,l3]]
	nc.close()


	mj,mn,ic,rmj,rmn,ric = [],[],[],[],[],[]
	for i in range(3):
		mjk,mnk,ick = ellipse(u[i],v[i],up[i],vp[i])
		mj.append(mjk); mn.append(mnk); ic.append(ick)
		rmjk,rmnk,rick = ellipse(uu[i],vv[i],rup[i],rvp[i])
		rmj.append(rmjk); rmn.append(rmnk); ric.append(rick)

	fig = plt.figure(figsize=(12, 4))

	gs1 = gridspec.GridSpec(1, 3)
	gs1.update(left=0.05, right=0.95, wspace=0.2)

	for i in range(3):
		pts = get_ellipse_coords(a=rmj[i], b=rmn[i], x=0, y=0, angle=-ric[i], k=2)
		ptsz = get_ellipse_coords(a=mj[i], b=mn[i], x=0, y=0, angle=-ic[i], k=2)
		plt.subplot(gs1[0, i]).plot(pts[:,0], pts[:,1],label='ROMS')
		plt.subplot(gs1[0, i]).plot(ptsz[:,0], ptsz[:,1],label='VLIZ')
		plt.xlim([-1.0,1.0])
		plt.ylim([-1.0,1.0])
		plt.xticks(ticks)
		plt.yticks(ticks)
		plt.legend(loc=2)
		#plt.axis('equal')

	fig.savefig('Ellipse_plot_M2_one_row_%s' %(name), dpi=200)


name=['NN','OW','OWc','TW','TWc']
for i in range(5):
	func(name[i])
