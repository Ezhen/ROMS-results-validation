import numpy as np; import matplotlib.pyplot as plt; import matplotlib as mpl; import matplotlib.patches as mpatches; from pylab import setp; import math

def current_rose_VLIZ(w,theta):
	###########################################################################################################
	#####################		Percentage of currents by directions		###########################
	###########################################################################################################
	x = [[] for i in range(72)]; procent=np.zeros((len(x)));procent_theta=np.zeros((len(x)))
	for i in range(len(w)):
		x[int(np.degrees(theta[i])/5.)].append(w[i])
	for i in range(len(x)):
		procent[i]=100.*len(x[i])/len(w)
		procent_theta[i]=i*5
	print procent
	print procent_theta
	###########################################################################################################
	#####################		Angles of currents from the new axes		###########################
	###########################################################################################################
	theta=3.1415/2+3.1415*2-theta
	procent_theta=90+360-procent_theta
	###########################################################################################################
	#####################		Making the basis for steteo plot		###########################
	###########################################################################################################
	#radii = 10 * np.random.rand(N)
	#width = np.pi / 4 * np.random.rand(N)
	fig = plt.figure(figsize=(12, 12))
	ax = plt.subplot(111, projection='polar',axisbg='#d5de9c')
	ax.set_theta_zero_location("N")
	ax.set_theta_direction(-1)
	ax.grid(False)
	for xmin in ax.xaxis.get_majorticklocs():
		#print xmin
		if xmin>1.57 and xmin<1.58:
			ax.axvline(x=xmin,ls='-', color='black')
			break
	for ymin in ax.yaxis.get_majorticklocs():
		ax.axhline(y=ymin,ls='--') 
	#ax.set_yticklabels([str(ax.yaxis.get_ticklabels()[0].get_text())+"%",str(ax.yaxis.get_ticklabels()[1].get_text())+"%",str(ax.yaxis.get_ticklabels()[2].get_text())+"%",str(ax.yaxis.get_ticklabels()[3].get_text())+"%",str(ax.yaxis.get_ticklabels()[4].get_text())+"%"])
	ax.set_yticklabels(['','1%','2%','3%','4%','5%','6%','7%', '8%','9%','10%','11%','12%','13%','14'])
	ax.grid(which='Major')
	ax.set_xticks(np.linspace(0,360,73)*6.28/360)
	ii=0
	for label in ax.xaxis.get_ticklabels()[0:-1]:
		label.set_visible(False)
		plt.axvline(ii,0.95,1.0, linestyle='-', color='black')
		ii=ii+5*3.1415*2/360
	for label in ax.xaxis.get_ticklabels()[::9]:
		label.set_visible(True)
		label.set_weight('bold')
	ax.xaxis.get_ticklabels()[-1].set_visible(False)
	###########################################################################################################
	######		Percent of currents by speed inside of each "direction" array		##################
	###########################################################################################################
	data = np.array([0,0.25,0.5,0.75,1.0,1.25])
	pr=np.zeros((len(procent),6))
	for i in range(len(procent)):
		if procent[i]==0:
			pr[i]=0#; print i
		else:
			a=np.array(x[i])
			pr[i,0]=len(a[a<data[1]])/float(len(a))*procent[i]
			pr[i,1]=len(a[(a>data[1]) & (a<data[2])])/float(len(a))*procent[i]
			pr[i,2]=len(a[(a>data[2]) & (a<data[3])])/float(len(a))*procent[i]
			pr[i,3]=len(a[(a>data[3]) & (a<data[4])])/float(len(a))*procent[i]
			pr[i,4]=len(a[(a>data[4]) & (a<data[5])])/float(len(a))*procent[i]
			pr[i,5]=len(a[a>data[5]])/float(len(a))*procent[i]
			#print i, sum(pr[i]),procent[i]
	cmap = plt.cm.gray_r
	norm = plt.Normalize(data.min(), data.max())
	colord = cmap(norm(data))
	ax.bar(procent_theta*3.1415/180, pr[:,0], color=colord[0], width=6.28/72)
	ax.bar(procent_theta*3.1415/180, pr[:,1], color=colord[1], width=6.28/72, bottom=pr[:,0])
	ax.bar(procent_theta*3.1415/180, pr[:,2], color=colord[2], width=6.28/72, bottom=pr[:,0]+pr[:,1])
	ax.bar(procent_theta*3.1415/180, pr[:,3], color=colord[3], width=6.28/72, bottom=pr[:,0]+pr[:,1]+pr[:,2])
	ax.bar(procent_theta*3.1415/180, pr[:,4], color=colord[4], width=6.28/72, bottom=pr[:,0]+pr[:,1]+pr[:,2]+pr[:,3])
	ax.bar(procent_theta*3.1415/180, pr[:,5], color=colord[5], width=6.28/72, bottom=pr[:,0]+pr[:,1]+pr[:,2]+pr[:,3]+pr[:,4])
	###########################################################################################################
	#####################			Data plotting		###########################################
	###########################################################################################################
	l1 = mpatches.Patch(color=colord[0], ec='black', label='$>$0-0.25')
	l2 = mpatches.Patch(color=colord[1], ec='black', label='0.25-0.5')
	l3 = mpatches.Patch(color=colord[2], ec='black', label='0.5-0.75')
	l4 = mpatches.Patch(color=colord[3], ec='black', label='0.75-1')
	l5 = mpatches.Patch(color=colord[4], ec='black', label='1-1.25')
	l6 = mpatches.Patch(color=colord[5], ec='black', label=r'$>$1.25')
	aaa=plt.legend(bbox_to_anchor = [0.35, 0.80],title='  \nCurrents (ms-1)',prop={'family':'Times New Roman','size':16},handles=[l1,l2,l3,l4,l5,l6]) # 0.85, 0.45
	setp(aaa.get_title(), fontsize=16, family='Times New Roman')
	aaa.get_frame().set_facecolor('#d5de9c');aaa.get_frame().set_alpha(0.0)#; aaa.get_frame().set_edgecolor('None')
	ax.set_rticks(list(np.arange(int(ax.get_rmax()))))  # less radial ticks
	ax.set_rlabel_position(90)  # get radial labels away from plotted line
	fig.savefig('1.png', dpi=80, bbox_inches='tight')#, transparent=True)
	#plt.show()

