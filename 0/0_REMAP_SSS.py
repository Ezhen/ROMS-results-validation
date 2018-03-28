import pyroms; from Get_grid import Get_grid_Mercator_Nest; from Get_grid import Get_grid_Mercator_Parent; from make_remap_grid_file import make_remap_grid_file; from remap import remap

src_grd_file = '/media/sf_Swap-between-windows-linux/New_Grid/TEMP_SALT_CURR_2004_2014.nc'
dst_grd_file = 'Salt_Surf_One_Parent.nc'

srcgrd = Get_grid_Mercator_Parent(src_grd_file)
dstgrd = pyroms.grid.get_ROMS_grid('COARSEST')

make_remap_grid_file(srcgrd)
pyroms.remapping.make_remap_grid_file(dstgrd, Cpos='rho')

# compute remap weights input namelist variables for bilinear remapping at rho points
grid1_file = 'remap_grid_MERCATOR_PARENT_t.nc'
grid2_file = 'remap_grid_COARSEST_rho.nc'
interp_file1 = 'remap_weights_MERCATOR_PARENT_to_COARSEST_bilinear_t_to_rho.nc'
interp_file2 = 'remap_weights_COARSEST_to_MERCATOR_PARENT_bilinear_rho_to_t.nc'
map1_name = 'MERCATOR_PARENT to COARSEST Bilinear Mapping'
map2_name = 'COARSEST to MERCATOR_PARENT Bilinear Mapping'
num_maps = 1
map_method = 'bilinear'
pyroms.remapping.compute_remap_weights(grid2_file, grid1_file, interp_file2, interp_file1, map2_name, map1_name, num_maps, map_method)


tart=0; tend=1095*24
wts='remap_weights_COARSEST_to_MERCATOR_PARENT_bilinear_rho_to_t.nc'
remap(tart, tend, dst_grd_file, 'salt', wts, dstgrd, srcgrd, src_grd_file, dst_dir='./')
