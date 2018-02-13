import numpy as np; import pyroms; from netCDF4 import Dataset; from mpl_toolkits.basemap import pyproj; from functions import point_inside_polygon
from Grid_VALID import Grid_VALID

poly=[(50.531,1.7312),(51.4691,3.7075),(52.5049,2.4314),(51.5905,0.4607)]
poly_parent=[(48.5,-0.4),(51.9,6.7),(54.9,2.8),(51.7,-4.3)]

def Get_grid_ODYSSEA_Nest(grdfile, name='ODYSSEA_NEST'):
    nc = Dataset(grdfile)
    lon = nc.variables['lon'][:]; lat = nc.variables['lat'][:]; var = nc.variables['sst'][0,:,:]
    nc.close()	
    lon,lat=np.meshgrid(lon,lat)
    lon_t = lon[:,:]
    lat_t = lat[:,:]
    lon_vert = 0.5 * (lon[:,1:] + lon[:,:-1])
    lon_vert = 0.5 * (lon_vert[1:,:] + lon_vert[:-1,:])
    lat_vert = 0.5 * (lat[1:,:] + lat[:-1,:])
    lat_vert = 0.5 * (lat_vert[:,1:] + lat_vert[:,:-1])
    #mask_t = np.ones((len(var[:,0]), len(var[0,:])))
    a=np.ones((len(var),len(var.T)))
    a[var.mask==True]=0
    #print a
    mask_t=a
    #mask correction
    for i in range(len(var)):
        for j in range(len(var.T)):
	    if point_inside_polygon(lat[i,j],lon[i,j],poly)==False:
		mask_t[i,j]=0
    z_t = 1; h=1
    geod = pyproj.Geod(ellps='WGS84')
    az_forward, az_back, dx = geod.inv(lon_vert[:,:-1], lat_vert[:,:-1], lon_vert[:,1:], lat_vert[:,1:])
    angle = 0.5 * (az_forward[1:,:] + az_forward[:-1,:])
    angle = (90 - angle) * np.pi/180.
    return Grid_VALID(lon_t, lat_t, lon_vert, lat_vert, mask_t, z_t, h, angle, name)

def Get_grid_Mercator_Nest(grdfile, name='MERCATOR_NEST'):
    nc = Dataset(grdfile)
    lon = nc.variables['lon'][44:74]; lat = nc.variables['lat'][31:62]; var = nc.variables['votemper'][0,0,31:62,44:74]#; depth = nc.variables['depth'][:]
    print np.shape(lon),np.shape(lat), np.shape(var)
    nc.close()	
    lon,lat=np.meshgrid(lon,lat)
    lon_t = lon[:,:]
    lat_t = lat[:,:]
    lon_vert = 0.5 * (lon[:,1:] + lon[:,:-1])
    lon_vert = 0.5 * (lon_vert[1:,:] + lon_vert[:-1,:])
    lat_vert = 0.5 * (lat[1:,:] + lat[:-1,:])
    lat_vert = 0.5 * (lat_vert[:,1:] + lat_vert[:,:-1])
    #mask_t = np.array(~var[:].mask, dtype='int')
    a=np.ones((len(var),len(var.T)))
    a[var.mask==True]=0
    #print a
    mask_t=a
    #mask correction
    for i in range(len(var)):
        for j in range(len(var.T)):
	    if point_inside_polygon(lat[i,j],lon[i,j],poly)==False:
		mask_t[i,j]=0
    #z_t = np.tile(depth,(mask_t.shape[2],mask_t.shape[1],1)).T
    #depth_bnds = np.zeros(len(depth)+1)
    #for i in range(1,len(depth)):
    #    depth_bnds[i] = 0.5 * (depth[i-1] + depth[i])
    #depth_bnds[-1] = 1000
    #bottom = pyroms.utility.get_bottom(var[::-1,:,:], mask_t[0], spval=var.fill_value)
    #nlev = len(depth)
    #bottom = (nlev-1) - bottom
    #h = np.zeros(mask_t[0,:].shape)
    #for i in range(mask_t[0,:].shape[1]):
    #    for j in range(mask_t[0,:].shape[0]):
    #        if mask_t[0,j,i] == 1:
    #            h[j,i] = depth_bnds[bottom[j,i]+1]
    z_t = 1; h=1
    geod = pyproj.Geod(ellps='WGS84')
    az_forward, az_back, dx = geod.inv(lon_vert[:,:-1], lat_vert[:,:-1], lon_vert[:,1:], lat_vert[:,1:])
    angle = 0.5 * (az_forward[1:,:] + az_forward[:-1,:])
    angle = (90 - angle) * np.pi/180.
    return Grid_VALID(lon_t, lat_t, lon_vert, lat_vert, mask_t, z_t, h, angle, name)

def Get_grid_ODYSSEA_Parent(grdfile, name='ODYSSEA_PARENT'):
    nc = Dataset(grdfile)
    lon = nc.variables['lon'][:]; lat = nc.variables['lat'][:]; var = nc.variables['sst'][0,:,:]
    nc.close()	
    lon,lat=np.meshgrid(lon,lat)
    lon_t = lon[:,:]
    lat_t = lat[:,:]
    lon_vert = 0.5 * (lon[:,1:] + lon[:,:-1])
    lon_vert = 0.5 * (lon_vert[1:,:] + lon_vert[:-1,:])
    lat_vert = 0.5 * (lat[1:,:] + lat[:-1,:])
    lat_vert = 0.5 * (lat_vert[:,1:] + lat_vert[:,:-1])
    a=np.ones((len(var),len(var.T)))
    a[var.mask==True]=0
    mask_t=a
    for i in range(len(var)):
        for j in range(len(var.T)):
	    if point_inside_polygon(lat[i,j],lon[i,j],poly_parent)==False:
		mask_t[i,j]=0
    z_t = 1; h=1
    geod = pyproj.Geod(ellps='WGS84')
    az_forward, az_back, dx = geod.inv(lon_vert[:,:-1], lat_vert[:,:-1], lon_vert[:,1:], lat_vert[:,1:])
    angle = 0.5 * (az_forward[1:,:] + az_forward[:-1,:])
    angle = (90 - angle) * np.pi/180.
    return Grid_VALID(lon_t, lat_t, lon_vert, lat_vert, mask_t, z_t, h, angle, name)

def Get_grid_Mercator_Parent(grdfile, name='MERCATOR_PARENT'):
    nc = Dataset(grdfile)
    lon = nc.variables['lon'][44:74]; lat = nc.variables['lat'][31:62]; var = nc.variables['votemper'][0,0,31:62,44:74]#; depth = nc.variables['depth'][:]
    print np.shape(lon),np.shape(lat), np.shape(var)
    nc.close()	
    lon,lat=np.meshgrid(lon,lat)
    lon_t = lon[:,:]
    lat_t = lat[:,:]
    lon_vert = 0.5 * (lon[:,1:] + lon[:,:-1])
    lon_vert = 0.5 * (lon_vert[1:,:] + lon_vert[:-1,:])
    lat_vert = 0.5 * (lat[1:,:] + lat[:-1,:])
    lat_vert = 0.5 * (lat_vert[:,1:] + lat_vert[:,:-1])
    a=np.ones((len(var),len(var.T)))
    a[var.mask==True]=0
    mask_t=a
    for i in range(len(var)):
        for j in range(len(var.T)):
	    if point_inside_polygon(lat[i,j],lon[i,j],poly_parent)==False:
		mask_t[i,j]=0
    z_t = 1; h=1
    geod = pyproj.Geod(ellps='WGS84')
    az_forward, az_back, dx = geod.inv(lon_vert[:,:-1], lat_vert[:,:-1], lon_vert[:,1:], lat_vert[:,1:])
    angle = 0.5 * (az_forward[1:,:] + az_forward[:-1,:])
    angle = (90 - angle) * np.pi/180.
    return Grid_VALID(lon_t, lat_t, lon_vert, lat_vert, mask_t, z_t, h, angle, name)


