import numpy as np; import matplotlib.pyplot as plt

def appendf(dir_num,n1,n2,line):
	try:
		dir_num.append(float(line[n1:n2]))
	except:
		dir_num.append(0)#(NaN / 0)
	return dir_num

curr1m1=[]; curr2m1=[]; curr3m1=[]; curr4m1=[]; curr5m1=[]; curr6m1=[];  curr1m3=[]; curr2m3=[]; curr3m3=[]; curr4m3=[]; curr5m3=[]; curr6m3=[]

for line in open('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20060101_20141231_MP0_Current.txt','r').readlines()[2::24]:
	try:
		a = float(line[39:43])
		b = float(line[57:61])
		c = float(line[75:79])
		if a<3 and b<3 and c<3:
			appendf(curr1m1,39,43,line); appendf(curr2m1,57,61,line); appendf(curr3m1,75,79,line); appendf(curr4m1,93,97,line); appendf(curr5m1,111,115,line); appendf(curr6m1,129,133,line)
	except:
		pass

for line in open('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20081001_20141231_MP4_Current.txt','r').readlines()[2::24]:
	try:
		a = float(line[39:43])
		b = float(line[57:61])
		c = float(line[75:79])
		if a<3 and b<3 and c<3:
			appendf(curr1m3,39,43,line); appendf(curr2m3,57,61,line); appendf(curr3m3,75,79,line); appendf(curr4m3,93,97,line); appendf(curr5m3,111,115,line); appendf(curr6m3,129,133,line)
	except:
		pass

c1m1,c2m1,c3m1,c4m1,c5m1,c6m1 = np.array(curr1m1),np.array(curr2m1),np.array(curr3m1),np.array(curr4m1),np.array(curr5m1),np.array(curr6m1)
m1m1,m2m1,m3m1,m4m1,m5m1,m6m1 = np.nanmean(c1m1),np.nanmean(c2m1),np.nanmean(c3m1),np.nanmean(c4m1),np.nanmean(c5m1),np.nanmean(c6m1)

c1m3,c2m3,c3m3,c4m3,c5m3,c6m3 = np.array(curr1m3),np.array(curr2m3),np.array(curr3m3),np.array(curr4m3),np.array(curr5m3),np.array(curr6m3)
m1m3,m2m3,m3m3,m4m3,m5m3,m6m3 = np.nanmean(c1m3),np.nanmean(c2m3),np.nanmean(c3m3),np.nanmean(c4m3),np.nanmean(c5m3),np.nanmean(c6m3)

m1 = [m1m1, m2m1, m3m1, m4m1, m5m1, m6m1]
m3 = [m1m3, m2m3, m3m3, m4m3, m5m3, m6m3]
h13 = [-0.75,-2.5,-5,-7.5,-10,-12.5]



time=[]; height=[]; kk=0; t=[]; corr_time=[]; curr1=[]; curr2=[];  curr3=[]; curr4=[]; curr5=[]; curr6=[]
for line in open('/home/eivanov/coawst_data_prrocessing/GRID_RECTANGULAR/Validation_VLIZ_Data/20060101_20141231_MP3_Current.txt','r').readlines()[2::24]:	
	try:
		a = float(line[39:43])
		b = float(line[66:70])
		if a<3 and b<3:
			time.append(line[0:16]); kk=kk+1; appendf(height,18,25,line)
			appendf(curr1,39,43,line); appendf(curr3,66,70,line); appendf(curr4,84,88,line); appendf(curr5,102,106,line); appendf(curr6,120,126,line)
	except:
		pass

c1,c3,c4,c5,c6 = np.array(curr1),np.array(curr3),np.array(curr4),np.array(curr5),np.array(curr6)
m1m2,m3m2,m4m2,m5m2,m6m2 = np.nanmean(c1),np.nanmean(c3),np.nanmean(c4),np.nanmean(c5),np.nanmean(c6)

m2 = [m1m2, m3m2, m4m2, m5m2, m6m2]
h2 = [-0.75,-5,-7.5,-10,-12.5]

fig, ax = plt.subplots(figsize=(12, 8))
plt.plot(m1,h13, label = 'MP0') 
plt.plot(m2,h2, label = 'MP3') 
plt.plot(m3,h13, label = 'MP4') 
plt.xlabel('Speed [m/s]'); plt.legend(loc=2); plt.xlim(0,0.8); plt.ylim(-9,0); plt.ylabel('Depth [m]'); fig.savefig('VLIZ_vertical_vel.png', dpi=100); plt.show()

