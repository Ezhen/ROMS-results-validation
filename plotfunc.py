import numpy as np; import matplotlib.pyplot as plt; from TaylorDiagram import TaylorDiagram

def plotfunc(olist,rlist,name,var,dop,temptype):

    refstd=np.zeros((len(olist)))
    # Reference dataset
    for i in range(len(olist)):
    	x = np.array(olist[i])
    	refstd[i] = x.std(ddof=1)           # Reference standard deviation

    # Compute stddev and correlation coefficient of models
    samples = np.array([ [np.array(m).std(ddof=1)/refstd[i], np.corrcoef(np.array(olist[i]), np.array(m))[0,1]]
                         for i,m in enumerate(tuple(rlist))])

    colors = plt.matplotlib.cm.jet(np.linspace(0,1,len(samples)))
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
    for i,(stddev,corrcoef) in enumerate(samples):
        dia.add_sample(stddev, corrcoef, marker='s', ls='', c=colors[i], label="%s" % (name[i]))

    # Add RMS contours, and label them
    contours = dia.add_contours(colors='0.5')
    plt.clabel(contours,  inline=1, fontsize=10)

    # Add a figure legend
    fig.legend(dia.samplePoints,
               [ p.get_label() for p in dia.samplePoints ],
               numpoints=1, prop=dict(size='small'), loc='upper right', title=var)
    fig.savefig('/home/eivanov/coawst_data_prrocessing/Temporal/Spatial_vaidation_tracers/Image_'+var+'_'+temptype+'.png')
    #plt.show()
