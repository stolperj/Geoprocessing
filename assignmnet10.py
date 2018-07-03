# ####################################### LOAD REQUIRED LIBRARIES
############################################# #
import time
import gdal
import numpy as np
import os
# ####################################### SET TIME-COUNT
###################################################### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time:" +  starttime)
print("")
# ####################################### FOLDER PATHS AND BASIC VARIABLES
#################################### #
rootFolder = "/Users/user/Downloads/Assignment10_data"
windowSize_px = [11, 21, 31]
drvR = gdal.GetDriverByName("GTiff")
# ####################################### FUNCTIONS
########################################################### #
def calcSHDI(array):
        arraySize = array.size
        SHDI = 0
        vals = [1, 2, 3, 5]
        array = np.where(array == 17, 1, array)  # reclassify open woodlands into forest
        for val in vals:
                count = (array == val).sum()
                # Check if value in in there, if not (i.e., count=0) then skip, because otherwise the ln will not be calculated
                if count > 0:
                    prop = count / arraySize
                    SHDI = SHDI + (prop * np.log(prop))
                else:
                    SHDI = - SHDI
        SHDI = SHDI
        return SHDI

def GetFilesInFolderWithEnding(folder, ext, fullPath):
    ''' Function that returns all filenames in a folder that match the extension
            Parameters
	    ----------
	    folder : string (required)
		    path, through which we are searching
	    ext : string (required)
		    extension of the files that we want to search for
	    fullPath : bool (required)
		    option to return just the file names or the entire file path
		    if True, then all matched files are concatenated with 'folder'
	    Returns
	    -------
	    outlist : list of strings
            CAUTION: if len(outlist) == 1, then outlist is a variable, will be returned with a print-statement
    '''

    outlist = []
    input_list = os.listdir(folder)
    if fullPath == True:
        for file in input_list:
            if file.endswith(ext):# Check if the variable folder ends with a '/', otherwise manually add to get correct path
                if folder.endswith("/"):
                    filepath = folder + file
                else:
                    filepath = folder + "/" + file
                outlist.append(filepath)
    if fullPath == False or fullPath == None:
        for file in input_list:
            if file.endswith(ext):
                outlist.append(file)
    if len(outlist) == 1:
        print("Found only one file matching the extension. Returning a variable instead of a list")
        outlist = outlist[0]
    if len(outlist) == 0:
        print("Could not find any file matching the extension. Return-value is None")
    return outlist
# ####################################### START PROCESSING #################################################### #
# (1) get the number of files
rasters = GetFilesInFolderWithEnding(rootFolder, ".tif", fullPath=True)
for raster in rasters:
    print("Processing raster: ", raster)
    ds = gdal.Open(raster)
    gt = ds.GetGeoTransform()
    pr = ds.GetProjection()
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    ds_array = ds.GetRasterBand(1).ReadAsArray(0, 0, cols, rows)# (2) Loop through the different radia
    for rad in windowSize_px:
        print("window-size: ", str(rad))# Define offset in x- and y-direction
        offset_xy = int(rad / 2)# Build the output array
        startRow = int(rad / 2)
        startCol = int(rad / 2)
        endRow = rows - startRow - 1
        endCol = cols - startCol - 1
        dim01_y = endRow - startRow  # nr. of indices in y-direction
        dim01_x = endCol - startCol  # nr. of indices in x-direction
        dim02 = rad * rad  # window-size
        sliced_array = np.zeros((dim01_y * dim01_x, dim02), dtype=np.float)
    # Populate the array
        index = 0  # set a manual counter to step through the different slices
        for row in range(startRow, endRow):
            for col in range(startCol, endCol):
                # calculate array coordinates of corner
                y_min = row - offset_xy
                y_max = row - offset_xy + rad
                x_min = col - offset_xy
                x_max = col - offset_xy + rad
                # print(x_min, y_min, x_max, y_max)
                # with .flatten() you remove any dimensions from your ndarray
                sliced_array[index, :] = ds_array[y_min: y_max, x_min: x_max].flatten()
                index += 1
                # calculate the index based on the function
            SHDI = np.apply_along_axis(calcSHDI, 1, sliced_array)
            # reshape and write to output-array
            SHDI = np.reshape(SHDI, ((endRow - startRow), (endCol - startCol)))
            out_array = np.zeros((rows, cols), dtype=float)
            out_array[startRow:endRow, startCol:endCol] = SHDI
            # write to output
            outname = raster
            outname = outname.replace(".tif", "_SHDI_" + str(rad) + ".tif")
            SHDI_out = drvR.Create(outname, cols, rows, 1, gdal.GDT_Float32)
            SHDI_out.SetProjection(pr)
            SHDI_out.SetGeoTransform(gt)
            SHDI_out.GetRasterBand(1).WriteArray(out_array, 0, 0)
# ####################################### END TIME-COUNT AND PRINT TIME STATS  ################################## #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")