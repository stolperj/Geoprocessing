#imports
import time
from osgeo import gdal
import pandas as pd
import ogr
import geopandas as gpd
import gdal

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# Script
#import data
wd = '/Users/juliastolper/Downloads/Assignment07_data/'

points_dir = wd+'Points.shp'
forest_dir = wd+'Old_Growth.shp'
private_dir = wd+'PrivateLands.shp'

POINTS = gpd.read_file(points_dir)
print('points prj:',POINTS.crs) #{'init': 'epsg:4326'}
shapedriver = ogr.GetDriverByName('ESRI SHAPEFILE')
points_open = shapedriver.Open(points_dir)
points = points_open.GetLayer()
npoints = points.GetFeatureCount()
print('count points:',npoints)

FOREST = gpd.read_file(forest_dir)
print('forest prj:',FOREST.crs)
FOREST = FOREST.to_crs({'init': 'epsg:4326'})
FOREST.to_file(wd+'forest_4326')
forest1_dir = wd+'forest_4326'
forest_open = shapedriver.Open(forest1_dir)
forest = forest_open.GetLayer()
nforest = forest.GetFeatureCount()
print('count forest:',nforest)

PRIVATE = gpd.read_file(private_dir)
print('private prj:',PRIVATE.crs)
PRIVATE = PRIVATE.to_crs({'init': 'epsg:4326'})
PRIVATE.to_file(wd+'private_4326')
private1_dir = wd+'private_4326'
private_open = shapedriver.Open(private1_dir)
private = private_open.GetLayer()
nprivate = private.GetFeatureCount()
print('count private:',nprivate)

elevation = wd+'Elevation.tif'
roadsx = wd+'DistToRoad.tif'
input_raster = gdal.Open(roadsx)
output_raster = wd + 'roads_4326.tif'
gdal.Warp(output_raster,input_raster,dstSRS='EPSG:4326')
roads = wd+'roads_4326.tif'

#functions
def get_value_at_point(raster, point):
    geom = point.GetGeometryRef()
    mx, my = geom.GetX(), geom.GetY()
    ds = gdal.Open(raster)
    pr = ds.GetProjection()
    gt = ds.GetGeoTransform()
    px = int((mx - gt[0]) / gt[1])
    py = int((my - gt[3]) / gt[5])
    rb = ds.GetRasterBand(1)
    #print(rb.DataType)
    val = rb.ReadAsArray(px, py, 1, 1)
    Value.append(val)

#processing
PointID = []
Variable = []
Value = []
point = points.GetNextFeature()
index = 0

while point:
  index += 1
  print (index,'of 2499')
  p = ogr.Geometry(ogr.wkbPoint)
  geom = point.GetGeometryRef()
  p.AddPoint(geom.GetX(), geom.GetY())
  PointID.append(index)
  Variable.append('Private')
  private_value = []
  priva = private.GetNextFeature()
  while priva:
    priv = priva.GetGeometryRef()
    if priv.Contains(p):  # check if in private
      private_value.append(1)
      priva = private.GetNextFeature()
    else:
      private_value.append(0)
      priva = private.GetNextFeature()
  Value.append(sum(private_value))
  PointID.append(index)
  Variable.append('OldGrowth')
  forest_value = []
  fores = forest.GetNextFeature()
  while fores:
    fore = fores.GetGeometryRef()
    if fore.Contains(p):  # check if in private
      forest_value.append(1)
      fores = forest.GetNextFeature()
    else:
      forest_value.append(0)
      fores = forest.GetNextFeature()
  Value.append(sum(forest_value))
  PointID.append(index)
  Variable.append('Elevation')
  get_value_at_point(elevation, point)
  PointID.append(index)
  Variable.append('Road_dist')
  get_value_at_point(roads, point)
  point = points.GetNextFeature()
points.ResetReading()

d = {'Point_ID': list(PointID), 'Variable': Variable, 'Value': Value}
df = pd.DataFrame(data=d)

df.to_csv(path_or_buf = wd+'output.csv', index = False)

# #### END TIME-COUNT AND PRINT TIME STATS #### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")