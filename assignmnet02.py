#imports
import os
import gdal
import time

# ####################################### SET TIME-COUNT ###################################################### #

starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# ####################################### FOLDER PATHS & global variables ##################################### #

root_folder = "/Users/juliastolper/Downloads/Week04 - Assignment/"

# ####################################### PROCESSING ########################################################## #
# (a) calculate the corner coordinates for each of the raster files
file_list = os.listdir(root_folder)
ULX=[]
ULY=[]
LRX=[]
LRY=[]
for file in file_list:
    ds = gdal.Open(root_folder + file, gdal.GA_ReadOnly)
    gt = ds.GetGeoTransform()#ULx,coordinates of end 1st pixel, ULy, coordinates of end 1st pixel
    #pr = ds.GetProjection()
    #cols = ds.RasterXSize
    #rows = ds.RasterYSize
    #print(cols,rows)
    UL_x, UL_y = gt[0], gt[3]#upper left
    ULX.append(UL_x)
    ULY.append(UL_y)
    #Lower right
    LR_x = UL_x + (gt[1]*ds.RasterXSize)
    LRX.append(LR_x)
    LR_y = UL_y + (gt[5]*ds.RasterYSize)
    LRY.append(LR_y)

#(b) find the overlapping area across all raster files
# UL_x max, UL_y_min, LR_x min, LR_y max
overlap=[]
overlap.append(max(ULX))
overlap.append(min(ULY))
overlap.append(min(LRX))
overlap.append(max(LRY))
print(overlap)
#Upper right
#URx=LRx, URy=ULy
#Lower left
#LLx=ULx, LLy=LRy
# ####################################### END TIME-COUNT AND PRINT TIME STATS################################## #

print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")