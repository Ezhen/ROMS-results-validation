import numpy as np; import matplotlib.pyplot as plt; from TaylorDiagram import TaylorDiagram

def plotfunc2(olist,olistc,rlist,rlistc,name,var,varc,dop,temptype):

    refstd=np.zeros((len(olist)))
    # Reference dataset
    for i in range(len(olist)):
    	x = np.array(olist[i])
    	refstd[i] = x.std(ddof=1)           # Reference standard deviation

    # Compute stddev and correlation coefficient of models
    samples = np.array([ [np.array(m).std(ddof=1)/refstd[i], np.corrcoef(np.array(olist[i]), np.array(m))[0,1]]
                         for i,m in enumerate(tuple(rlist))])
    samplesc = np.array([ [np.array(m).std(ddof=1)/refstd[i], np.corrcoef(np.array(olistc[i]), np.array(m))[0,1]]
                         for i,m in enumerate(tuple(rlistc))])

    colors = plt.matplotlib.cm.jet(np.linspace(0,1,len(samples)))
    colorsc = plt.matplotlib.cm.jet(np.linspace(0,1,len(samplesc)))
    """
    if dop == 'need_temporal':
    	fig = plt.figure(figsize=(15,6))
    	
    	ax1 = fig.add_subplot(1,2,1, xlabel='X', ylabel='Y')
    	# Taylor diagram
    	dia = TaylorDiagram(1, fig=fig, rect=122, label="Reference")

    	ax1.plot(np.arange(len(x)),x,'ko', label='Odyssea')
    	for i,m in enumerate(rlist):
    	    ax1.plot(np.arange(len(x)),m, c=colors[i], label='%s' % (name[i]))
    	ax1.legend(numpoints=1, prop=dict(size='small'), loc='best')
    """
    if dop == 'no_need':
    	fig = plt.figure(figsize=(8,6))
	dia = TaylorDiagram(1, fig=fig, label="Reference")

    # Add samples to Taylor diagram
    dia.add_sample(-200, -200, c='w',alpha=0,label="Grid:")
    dia.add_sample(-200, -200, marker='s', ls='', c="w", label="Parent")#,edgecolor=None)
    dia.add_sample(-200, -200, marker='o', ls='', c="w", label="Child")#, edgecolor=None)
    dia.add_sample(-200, -200, c='w',alpha=0,label="Months:")
    for i,(stddev,corrcoef) in enumerate(samples):
        dia.add_sample(stddev, corrcoef, marker='s', ls='', c=colors[i], label="%s" % (name[i]))
    for i,(stddev,corrcoef) in enumerate(samplesc):
        dia.add_sample(stddev, corrcoef, marker='o', ls='', c=colorsc[i])

    # Add RMS contours, and label them
    contours = dia.add_contours(colors='0.5')
    plt.clabel(contours,  inline=1, fontsize=10)
    contoursc = dia.add_contours(colors='0.5')
    plt.clabel(contoursc,  inline=1, fontsize=10)

    # Add a figure legend
    fig.legend(dia.samplePoints,
               [ p.get_label() for p in dia.samplePoints[0:17] ],
               numpoints=1, prop=dict(size='small'), ncol=1 ,loc='upper right', title=var[0:3])
    fig.savefig('/home/eivanov/coawst_data_prrocessing/Temporal/Spatial_vaidation_tracers/Image_old_same_grid_'+var+varc+'_'+temptype+'.png')
    #plt.show()
