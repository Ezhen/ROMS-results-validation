from pylab import *; import matplotlib.gridspec as gridspec; from netCDF4 import Dataset; from scipy import spatial;plt.rcParams["font.family"] = 'Times New Roman'; mpl.rcParams['axes.unicode_minus']=False

MP0_lat=51+23/60.+40.04/3600.; MP0_lon=3+2./60.+44.82/3600. # MP0 (Measuring Pile 0, Oostdyckbank)
MP3_lat=51+23/60.+22.57/3600.; MP3_lon=3+11/60.+55.42/3600. # MP3 (Measuring Pile 3, Westhinder)  
MP4_lat=51+25/60.+6.08/3600. ; MP4_lon=3+17/60.+54.88/3600. # MP4 (Measuring Pile 4, Westhinder)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

vliz_amplitude_plot=list([np.mean([1.626,1.638,1.62]),np.mean([0.465,0.465,0.458]),np.mean([0.275,0.275,0.271])])
vliz_phase_var_plot=list([np.mean([9.82,14.33,19.11]),np.mean([64.35,69.38,74.63]),np.mean([345.51,350.03,354.63])])
vliz_variation_plot=list([max([1.626,1.638,1.62])-min([1.626,1.638,1.62]),max([0.465,0.465,0.458])-min([0.465,0.465,0.458]),max([0.275,0.275,0.271])-min([0.275,0.275,0.271])])

def func(name):
	nc = Dataset('/home/eivanov/coawst_data_prrocessing/Temporal/Tides/%s_zeta_MPDATA.nc' %(name), 'r', format='NETCDF4')
	lats = nc.variables['lat'][:]; lons = nc.variables['lon'][:]
	aa=np.array((list(lons.flatten()), list(lats.flatten()))).T; 
	idxx=spatial.KDTree(aa).query([MP0_lon,MP0_lat])[1]; idxx3=spatial.KDTree(aa).query([MP3_lon,MP3_lat])[1]; idxx4=spatial.KDTree(aa).query([MP4_lon,MP4_lat])[1]; 
	k1=int(np.where(lons==aa[idxx][0])[0][0]); k2=int(np.where(lons==aa[idxx3][0])[0][0]); k3=int(np.where(lons==aa[idxx4][0])[0][0])
	l1=int(np.where(lons==aa[idxx][0])[1][0]); l2=int(np.where(lons==aa[idxx3][0])[1][0]); l3=int(np.where(lons==aa[idxx4][0])[1][0])
	m2 = [nc.variables['M2'][k1,l1],nc.variables['M2'][k2,l2],nc.variables['M2'][k3,l3]] 
	s2 = [nc.variables['S2'][k1,l1],nc.variables['S2'][k2,l2],nc.variables['S2'][k3,l3]] 
	n2 = [nc.variables['N2'][k1,l1],nc.variables['N2'][k2,l2],nc.variables['N2'][k3,l3]]
	m2p = [nc.variables['MP2'][k1,l1],nc.variables['MP2'][k2,l2],nc.variables['MP2'][k3,l3]]
	s2p = [nc.variables['SP2'][k1,l1],nc.variables['SP2'][k2,l2],nc.variables['SP2'][k3,l3]]
	n2p = [nc.variables['NP2'][k1,l1],nc.variables['NP2'][k2,l2],nc.variables['NP2'][k3,l3]]
	nc.close()

	roms_amplitude_plot=list([np.mean(m2),np.mean(s2),np.mean(n2)])
	roms_phase_var_plot=list([np.mean(m2p),np.mean(s2p),np.mean(n2p)])
	roms_variation_plot=list([max(m2)-min(m2),max(s2)-min(s2),max(n2)-min(n2)])

	fig = plt.figure(figsize=(8, 8))

	gs1 = gridspec.GridSpec(1, 3)
	gs1.update(left=0.15, right=0.95, wspace=0)
	ax1 = plt.subplot(gs1[:, :])

	#ax1 = fig.add_subplot(212)
	index = np.arange(3)
	bar_width = 0.35

	opacity = 0.4; error_config = {'ecolor': '0.3'}

	rects1 = ax1.bar(index, vliz_amplitude_plot, bar_width,alpha=opacity, color='b', yerr=vliz_variation_plot, error_kw=error_config, label='VLIZ')

	rects2 = ax1.bar(index + bar_width, roms_amplitude_plot, bar_width, alpha=opacity, color='r', yerr=roms_variation_plot, error_kw=error_config, label='ROMS')

	ax1.set_xlabel('Constituents'); ax1.set_ylabel('Amplitude [m]')#; plt.title('Comparison VLIZ and ROMS')
	ax1.set_xticks(index + bar_width )
	ax1.set_xticklabels(['M2','S2','N2'])
	ax1.legend()#title='%s' %(name))

	#plt.show()

	fig.savefig('/home/eivanov/coawst_data_prrocessing/Temporal/Tides/Bar_plot_%s' %(name), dpi=200)

name=['OW','OWc','TW','TWc']
for i in range(4):
	func(name[i])
