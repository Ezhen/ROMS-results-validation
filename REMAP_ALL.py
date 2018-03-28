import pyroms; from Get_grid import *; from make_remap_grid_file import make_remap_grid_file; from remap import remap; from nco import Nco; import subprocess,os,commands

src_grd_file1 = '/media/sf_Swap-between-windows-linux/DATA_INPUT_ROMS/Mercator/IFREMER-NWS-SST-L4-REP-OBS_FULL_TIME_SERIE_1520866230672.nc'
src_grd_file2 = '/media/sf_Swap-between-windows-linux/DATA_INPUT_ROMS/Mercator/TEMP_SALT_CURR_2004_2014.nc'

def func(dst_grd_file,order):
	if order=='PARENT':
		srcgrd1 = Get_grid_ODYSSEA_Parent(src_grd_file1)
		srcgrd2 = Get_grid_Mercator_Parent(src_grd_file2)
		grid='COARSEST'
		dstgrd = pyroms.grid.get_ROMS_grid(grid)
		pyroms.remapping.make_remap_grid_file(dstgrd, Cpos='rho')
	elif order=='NEST':
		srcgrd1 = Get_grid_ODYSSEA_Nest(src_grd_file1)
		srcgrd2 = Get_grid_Mercator_Nest(src_grd_file2)
		grid='FINER'
		dstgrd = pyroms.grid.get_ROMS_grid(grid)
		pyroms.remapping.make_remap_grid_file_2(dstgrd, Cpos='rho')

	#### Uncomment if you want to compute weights between two grid ####

	make_remap_grid_file(srcgrd1)
	make_remap_grid_file(srcgrd2)

	# compute remap weights input namelist variables for bilinear remapping at rho points
	grid1_file = 'remap_grid_ODYSSEA_%s_t.nc' %(order)
	grid2_file = 'remap_grid_%s_rho.nc' %(grid)
	interp_file1 = 'remap_weights_ODYSSEA_%s_to_%s_bilinear_t_to_rho.nc' %(order,grid)
	interp_file2 = 'remap_weights_%s_to_ODYSSEA_%s_bilinear_rho_to_t.nc' %(grid,order)
	map1_name = 'ODYSSEA_%s to %s Bilinear Mapping' %(order,grid)
	map2_name = '%s to ODYSSEA_%s Bilinear Mapping' %(grid,order)
	num_maps = 1
	map_method = 'bilinear'
	pyroms.remapping.compute_remap_weights(grid2_file, grid1_file, interp_file2, interp_file1, map2_name, map1_name, num_maps, map_method)

	grid1_file = 'remap_grid_MERCATOR_%s_t.nc' %(order)
	grid2_file = 'remap_grid_%s_rho.nc' %(grid)
	interp_file1 = 'remap_weights_MERCATOR_%s_to_%s_bilinear_t_to_rho.nc' %(order,grid)
	interp_file2 = 'remap_weights_%s_to_MERCATOR_%s_bilinear_rho_to_t.nc' %(grid,order)
	map1_name = 'MERCATOR_%s to %s Bilinear Mapping' %(order,grid)
	map2_name = '%s to MERCATOR_%s Bilinear Mapping' %(grid,order)
	num_maps = 1
	map_method = 'bilinear'
	pyroms.remapping.compute_remap_weights(grid2_file, grid1_file, interp_file2, interp_file1, map2_name, map1_name, num_maps, map_method)

	tt=365*3
        dst_grd_file = '/home/eivanov/coawst_data_prrocessing/Temporal/Former/' + dst_grd_file
	wts = 'remap_weights_%s_to_ODYSSEA_%s_bilinear_rho_to_t.nc' %(grid,order)
	remap(tt, dst_grd_file, 'sst', wts, dstgrd, srcgrd1, src_grd_file1,order,grid)

	wts = 'remap_weights_%s_to_MERCATOR_%s_bilinear_rho_to_t.nc' %(grid,order)
	remap(tt, dst_grd_file, 'sbt', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)
	remap(tt, dst_grd_file, 'sss', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)
	remap(tt, dst_grd_file, 'sbs', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)
	remap(tt, dst_grd_file, 'ssu', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)
	remap(tt, dst_grd_file, 'ssv', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)
	remap(tt, dst_grd_file, 'sbu', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)
	remap(tt, dst_grd_file, 'sbv', wts, dstgrd, srcgrd2, src_grd_file2,order,grid)

	a='sstODYSSEA_%s.nc' %(order)
	b='%s_sstODYSSEA_%s.nc' %(dst_grd_file[:-3],order)
	os.rename(a,b)

	ic_file = dst_grd_file[:-3]+'_replottedMERCATOR_%s.nc' %(order)
	cycle=['sbt','sss','sbs','ssu','ssv','sbu','sbv']
	for i in range(len(cycle)):
		out_file = '%sMERCATOR_%s.nc' %(cycle[i],order)
		command = ('ncks', '-a', '-A', out_file, ic_file) 
		subprocess.check_call(command)
		os.remove(out_file)

dst_grd_filei=['OW.nc','TW.nc','OWc.nc','TWc.nc']
orderi=['PARENT','PARENT','NEST','NEST']
for n in range(2,4):
	dst_grd_file = dst_grd_filei[n]
	order = orderi[n] 
	func(dst_grd_file,order)
