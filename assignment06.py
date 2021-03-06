#imports
import time
import os
import numpy as np
from osgeo import gdal
import ospybook as pb

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# Script
wd = '/Users/juliastolper/Downloads/Assignment06_data/'
tile1 = wd+'Tile_x17999_y20999_1000x1000.tif'
tile2 = wd+'Tile_x19999_y32999_1000x1000.tif'
tile3 = wd+'Tile_x26999_y12999_1000x1000.tif'

#from book chapter 11
def make_slices(data, win_size):
    """Return a list of slices given a window size.
    data     - two-dimensional array to get slices from
    win_size - tuple of (rows, columns) for the moving window
    """
    rows = data.shape[0] - win_size[0] + 1
    cols = data.shape[1] - win_size[1] + 1
    slices = []
    for i in range(win_size[0]):
      for j in range(win_size[1]):
        slices.append(data[i:rows+i, j:cols+j])
    return slices
''' # also in ospybook included
def make_raster(in_ds, fn, data, data_type, nodata=None):
    """Create a one-band GeoTIFF.
    in_ds     - datasource to copy projection and geotransform from
    fn        - path to the file to create
    data      - NumPy array containing data to write
    data_type - output data type
    nodata    - optional NoData value
    """
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
        fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    if nodata is not None:
        out_band.SetNoDataValue(nodata)
    out_band.WriteArray(data)
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    return out_ds
'''
#functions
def shdi(field):
    value = []
    cat_list =[1,17,2,3,5,11,13,18,19] # relevant categories
    dic = {}
    unique, counts = np.unique(field, return_counts=True)#all categories
    cat_count = dict(zip(unique, counts))# all numbers of all categories
    for cat in cat_list:
        if cat in cat_count:
            dic.update({cat: cat_count[cat]})
            cat_sum = sum(dic.values())
            prop = (dic[cat]/cat_sum)
            shdi = (prop * np.math.log10(prop))
            value.append(shdi)
    shdi_sum = sum(value) * (-1)
    return(shdi_sum)

def apply_shdi_150 (in_fn, out_fn150):
    in_ds = gdal.Open(in_fn)
    in_band = in_ds.GetRasterBand(1)
    in_data = in_band.ReadAsArray()
    slices = pb.make_slices(in_data, (11, 11))
    stacked_data = np.ma.dstack(slices)
    rows, cols = in_band.YSize, in_band.XSize
    out_data = np.ones((rows, cols), np.int32) * -99
    out_data[5:-5, 5:-5] = np.mean(stacked_data, 2)
    pb.make_raster(in_ds, out_fn150, out_data, gdal.GDT_Int32, -99)
    del in_ds
    print("shdi 150 executed")

def apply_shdi_300 (in_fn, out_fn300):
    in_ds = gdal.Open(in_fn)
    in_band = in_ds.GetRasterBand(1)
    in_data = in_band.ReadAsArray()
    slices = pb.make_slices(in_data, (21, 21))
    stacked_data = np.ma.dstack(slices)
    rows, cols = in_band.YSize, in_band.XSize
    out_data = np.ones((rows, cols), np.int32) * -99
    out_data[10:-10, 10:-10] = np.mean(stacked_data, 2)
    pb.make_raster(in_ds, out_fn300, out_data, gdal.GDT_Int32, -99)
    del in_ds
    print("shdi 300 executed")

def apply_shdi_450 (in_fn, out_fn450):
    in_ds = gdal.Open(in_fn)
    in_band = in_ds.GetRasterBand(1)
    in_data = in_band.ReadAsArray()
    slices = pb.make_slices(in_data, (31, 31))
    stacked_data = np.ma.dstack(slices)
    rows, cols = in_band.YSize, in_band.XSize
    out_data = np.ones((rows, cols), np.int32) * -99
    out_data[15:-15, 15:-15] = np.mean(stacked_data, 2)
    pb.make_raster(in_ds, out_fn450, out_data, gdal.GDT_Int32, -99)
    del in_ds
    print("shdi 450 executed")

#apply to rasters
t1150 = wd+'tile1_150.tif'
t1300 = wd+'tile1_300.tif'
t1450 = wd+'tile1_450.tif'
apply_shdi_150(tile1, t1150)
apply_shdi_300(tile1, t1300)
apply_shdi_450(tile1, t1450)
print("tile 1 completed")

t2150 = wd+'tile2_150.tif'
t2300 = wd+'tile2_300.tif'
t2450 = wd+'tile2_450.tif'
apply_shdi_150(tile2, t2150)
apply_shdi_300(tile2, t2300)
apply_shdi_450(tile2, t2450)
print("tile 2 completed")

t3150 = wd+'tile3_150.tif'
t3300 = wd+'tile3_300.tif'
t3450 = wd+'tile3_450.tif'
apply_shdi_150(tile3, t3150)
apply_shdi_300(tile3, t3300)
apply_shdi_450(tile3, t3450)
print("tile 3 completed")

# end time count
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")