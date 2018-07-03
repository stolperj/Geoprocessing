# load packages

import time
from osgeo import gdal, ogr, osr
import numpy as np
import struct

#set time

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

#define functions

def RasterOverlapToArray(file_list):#overlap from assignment4
    array_list = []
    ULX = []
    ULY = []
    LRX = []
    LRY = []
    for file in file_list:
        ds = gdal.Open(wd + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform()
        # pr = ds.GetProjection()
        # cols = ds.RasterXSize
        # rows = ds.RasterYSize
        # print(cols,rows)
        UL_x, UL_y = gt[0], gt[3]  # upper left
        ULX.append(UL_x)
        ULY.append(UL_y)
        # Lower right
        LR_x = UL_x + (gt[1] * ds.RasterXSize)
        LRX.append(LR_x)
        LR_y = UL_y + (gt[5] * ds.RasterYSize)
        LRY.append(LR_y)
    # (b) find the overlapping area across all raster files
    # UL_x max, UL_y_min, LR_x min, LR_y max
    overlap = []
    overlap.append(max(ULX))
    overlap.append(min(ULY))
    overlap.append(min(LRX))
    overlap.append(max(LRY))
    extent_x = int(round((min(LRX) - max(ULX))/gt[1])) #width of common extent/pixel width = number of columns
    extent_y = int(round(min(ULY) - max(LRY))/gt[1]) #height of common extent/pixel height = number of rows
    spat_res = [gt[1], abs(gt[5])]
    print(overlap)
    print(extent_x, extent_y)
    print(spat_res)
    for file in file_list:  #convert real-world coordinates (lat/lon) to image coordinates (x,y)
        print(file) #for overview in console
        ds = gdal.Open(wd + file, gdal.GA_ReadOnly)
        gt = ds.GetGeoTransform() #ULx,coordinates of end 1st pixel, ULy, coordinates of end 1st pixel
        inv_gt = gdal.InvGeoTransform(gt)  # geographic to array coordinates
        x1,y1 = gdal.ApplyGeoTransform(inv_gt, overlap[0], overlap[1])
        x2,y2 = gdal.ApplyGeoTransform(inv_gt, overlap[2], overlap[3])
        minX = int(round(min(x1,x2))) # x value for UL/origin
        minY = int(round(min(y1,y2))) # y value for UL/origin
        maxX = int(round(max(x1,x2))) # x value for LR
        maxY = int(round(max(y1,y2))) # y value for LR
        print("common extent: ", minX,maxX,minY,maxY) #cell coordinates
        x1off, y1off = map(int, [x1, y1]) # set upper left starting point for read as array
        array_list.append(ds.ReadAsArray(x1off, y1off, extent_x, extent_y)) #Upper Left corner
    return overlap,array_list

# script
wd = "C:/Users/PC-Pool/Downloads/data9/"

#imports
raster1 = "LE07_L1TP_117056_20040211_20170122_01_T1_sr_evi.tif"
raster2 = "LE07_L1TP_117056_20130627_20161124_01_T1_sr_evi.tif"
raster3 = "LT05_L1TP_117056_19980407_20161228_01_T1_sr_evi.tif"
raster4 = "LT05_L1TP_117056_20000717_20161214_01_T1_sr_evi.tif"

driver = ogr.GetDriverByName("ESRI Shapefile")
pts = driver.Open(wd + "RandomPoints.shp",1)
pts_lyr = pts.GetLayer()
n_pts = pts_lyr.GetFeatureCount()
#reproject points to match raster
source_SR = pts_lyr.GetSpatialRef()
ol = gdal.Open(wd + raster1)
pr_ol = ol.GetProjection()
target_SR_ol = osr.SpatialReference()
target_SR_ol.ImportFromWkt(pr_ol)
coordTrans_ol = osr.CoordinateTransformation(source_SR, target_SR_ol)

#raster file list as input for RasterOverlaptoArray function
file_list = [raster1, raster2, raster3, raster4]

#get raster overlap as array
overlap,array_list = RasterOverlapToArray(file_list)
#array_list = RasterOverlapToArray(file_list)
print(array_list)

#extract values from points
point_values = []
point_classes = []
feat = pts_lyr.GetNextFeature()
index = 0
while feat:
    values_pts = []
    index += 1
    print(index, "of", n_pts)

    #reproject
    coord = feat.GetGeometryRef()
    coord_cl = coord.Clone()
    coord_cl.Transform(coordTrans_ol)
    x, y = coord_cl.GetX(), coord_cl.GetY()

    # only extract values from points where points within overlap
    if overlap[0] <= x <= overlap[2]:#check if x point coordinate in overlap
        if overlap[3] <= y <= overlap[1]: #check if y point coordinate in overlap
            #save classes in list
            pt_class = feat.GetField('Class')
            print("Point class:", pt_class)
            point_classes.append(pt_class)

            for raster in file_list:

                #get_value_at_point(raster, point): function from assignment8

                ds = gdal.Open(wd+raster)
                gt = ds.GetGeoTransform()
                px = int((x - gt[0]) / gt[1])
                py = int((y - gt[3]) / gt[5])
                rb = ds.GetRasterBand(1)
                # print(rb.DataType)
                val = rb.ReadRaster(px, py, 1, 1)
                value = struct.unpack('H', val)# readasarray also ok???
                valuu = value[0]

                #save results for each raster in list
                values_pts.append(valuu)
                print("Point Values:", values_pts)

                point_values.append(values_pts)
    feat = pts_lyr.GetNextFeature()

pts_lyr.ResetReading()

#point values to array with 4 columns
values_array = np.asarray(point_values)
print("Array with values",values_array.shape)
#Array with values (3080, 4)

#point training values to array
classes_array = np.asarray(point_classes)
print("Array with classes ", classes_array.shape)
#Array with classes  (770,)

# Save the numpy arrays to disc
x_dim = values_array.shape[1]
y_dim = values_array.shape[0]
outName = "trainingDS_features_"+str(x_dim)+"_"+str(y_dim)+".npy"
np.save(outName, values_array)

x_dim = 1
y_dim = classes_array.shape[0]
outName = "trainingDS_labels_"+str(x_dim)+"_"+str(y_dim)+".npy"
np.save(outName, classes_array)

#make empty array
x_dim = array_list[0].shape[1]
y_dim = array_list[0].shape[0]
out_array = np.zeros((x_dim * y_dim, 4), dtype=np.int8)

# array sclicing of input arrays (overlaps)
for i in range(len(array_list)):
    out_array[:,i] = array_list[i].ravel() # ravel for 1 dimension
print("classificationDS_features ",out_array.shape)
#(2967888, 4) --> 2967888 rows and 4 columns

outName = "classificationDS_features_"+str(x_dim)+"_"+str(y_dim)+".npy"
np.save(outName, out_array)

# end time
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")