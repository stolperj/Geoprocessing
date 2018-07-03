'''
for list Pa
1. Get one PA
2. (N) Get extent of PA
3. (N) Random Point within based on starting point
4. (SP) Check if Point within borders of PA
5. Check if point has min x-meters distance to nearest border
6. Check if x-coord >= 90m if not check if y-coord >= 90m from pixels in list
both false start again, True save in list

Get vertices of polygons using the random point sample
function 'create_vertices'
create geometries from vertices
create features from geometries and gropu them with an identifier attbribute
Intersect NP, ,method=within
'''

import time
from osgeo import ogr
from osgeo import osr
import os
import numpy as np
import shapely
from shapely.geometry import Polygon, Point
import geopandas as gpd
from osgeo import gdal
import random
from shapely import wkt

'''
Comments: No Landsat center taken into consideration !
'''

# #### SET TIME-COUNT #### #
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

# Script
wd = '/Users/juliastolper/Downloads/Assignment05 - data/'
'''
#preprocessing 
lypa = wd+'WDPA_May2018_polygons_GER_select10large.shp'
lyp = wd+'OnePoint.shp'
pas = ogr.Open(lypa)
pl = pas.GetLayer()

ref = pl.GetSpatialRef()
print(ref) #GCS_WGS_1984, EPSG 4326

PA = gpd.read_file(lypa)
# Check original projection
PA.crs # out {'init': 'epsg:4326'}
PA = PA.to_crs({'init': 'epsg:3035'}) # Reproject to Lambert Azimuthal Equal Area
PA.to_file(wd+'PA_3035')
'''
#import equal area PA
lype = wd+'PA_3035/PA_3035.shp'
pes = ogr.Open(lype)
pe = pes.GetLayer()

ref_pe = pe.GetSpatialRef()
print(ref_pe) #PROJCS"ETRS89_LAEA_Europe"

###loop for points
all_points = []
Name_list = []

for feature in pe:
    NAME = feature.GetField("NAME")
    print(NAME)
    Name_list.append(NAME)
    geo = feature.GetGeometryRef()
    geo.GetEnvelope()
    (min_x, max_x, min_y, max_y) = geo.GetEnvelope()
    pol = Polygon([[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]])
    num_points = 50
    points = []
    min_x, min_y, max_x, max_y = pol.bounds
    while len(points) < num_points:
        random_point = Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
        if (random_point.within(pol)):
            randm_p = ogr.Geometry(ogr.wkbPoint)
            randm_p.AddPoint(random_point.x, random_point.y)
            if geo.Contains(randm_p):#check if in PA
                pa_line = wkt.loads(str(geo))
                point = wkt.loads(str(randm_p))
                if pa_line.boundary.distance(point) >= 64:#check if all polgons are in PA
                    points.append(random_point)
                    all_points.append(random_point)
        #for i in points: #print(i.x, i.y)
    print(points)

print(all_points)

# .SHP
# create a shapefile for polygons
driver = ogr.GetDriverByName('ESRI Shapefile')
shapefile = driver.CreateDataSource(wd+'jule.shp')
# set spatial reference
spatialreference = ref_pe
#create the layer
layer = shapefile.CreateLayer('jule', spatialreference, ogr.wkbPolygon)
layerDefinition = layer.GetLayerDefn()

# add attributes to layer
point_ID = ogr.FieldDefn('point_ID', ogr.OFTInteger)
polygon_ID = ogr.FieldDefn('polygon_ID', ogr.OFTInteger)
PA_name = ogr.FieldDefn('PA_name', ogr.OFTString)
layer.CreateField(point_ID)
layer.CreateField(polygon_ID)
layer.CreateField(PA_name)

# create kml file
driverkml = ogr.GetDriverByName('KML')
data_sourcekml = driverkml.CreateDataSource(wd+'jule.kml')
srskml = osr.SpatialReference()
srskml.ImportFromEPSG(3050)
layerkml = data_sourcekml.CreateLayer('jule', srskml, ogr.wkbPolygon)
layerkml.CreateField(point_ID)
layerkml.CreateField(polygon_ID)
layerkml.CreateField(PA_name)
defnkml = layerkml.GetLayerDefn()

index = 0

for i in all_points:
    index += 1
    if index <= 50:
            PA = Name_list[0]
    elif index in range(51,100):
            PA = Name_list [1]
    elif index in range(101, 150):
        PA = Name_list[2]
    elif index in range(151,200):
        PA = Name_list [3]
    elif index in range(201,250):
        PA = Name_list [4]
    elif index in range(251,300):
        PA = Name_list [5]
    elif index in range(301,350):
        PA = Name_list [6]
    elif index in range(351,400):
        PA = Name_list [7]
    elif index in range(401,450):
        PA = Name_list [8]
    else:
        PA = Name_list [9]
    #mid = Polygon([[i.x -15, i.y -15], [i.x +15, i.y -15], [i.x + 15, i.y +15], [i.x -15, i.y +15]])#test
    mid = ogr.Geometry(ogr.wkbLinearRing)
    mid.AddPoint(i.x -15, i.y -15)
    mid.AddPoint(i.x +15, i.y -15)
    mid.AddPoint(i.x + 15, i.y +15)
    mid.AddPoint(i.x -15, i.y +15)
    mid.AddPoint(i.x -15, i.y -15)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(mid)
    #put into shape
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 1)
    feature.SetField("PA_name" , str(PA))
    layer.CreateFeature(feature)
    #put into kml
    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 1)
    featkml.SetField("PA_name" , str(PA))
    layerkml.CreateFeature(featkml)
    #ul,um,ur,ri,lr,lm,ll,le
    ul = ogr.Geometry(ogr.wkbLinearRing)
    ul.AddPoint(i.x -45, i.y +45)
    ul.AddPoint(i.x -15, i.y +45)
    ul.AddPoint(i.x -15, i.y + 15)
    ul.AddPoint(i.x - 45, i.y + 15)
    ul.AddPoint(i.x - 45, i.y + 45)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ul)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 2)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 2)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #um
    um = ogr.Geometry(ogr.wkbLinearRing)
    um.AddPoint(i.x - 15, i.y +45)
    um.AddPoint(i.x + 15, i.y +45)
    um.AddPoint(i.x + 15, i.y + 15)
    um.AddPoint(i.x - 15, i.y + 15)
    um.AddPoint(i.x - 15, i.y +45)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(um)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 3)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 3)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #ur
    ur = ogr.Geometry(ogr.wkbLinearRing)
    ur.AddPoint(i.x + 15, i.y +45)
    ur.AddPoint(i.x + 45, i.y +45)
    ur.AddPoint(i.x + 45, i.y + 15)
    ur.AddPoint(i.x + 15, i.y + 15)
    ur.AddPoint(i.x + 15, i.y +45)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ur)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 4)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 4)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #ri
    ri = ogr.Geometry(ogr.wkbLinearRing)
    ri.AddPoint(i.x + 15, i.y + 15)
    ri.AddPoint(i.x + 45, i.y + 15)
    ri.AddPoint(i.x + 45, i.y - 15)
    ri.AddPoint(i.x + 15, i.y - 15)
    ri.AddPoint(i.x + 15, i.y +15)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ri)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 5)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 5)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #lr
    lr = ogr.Geometry(ogr.wkbLinearRing)
    lr.AddPoint(i.x + 15, i.y - 15)
    lr.AddPoint(i.x + 45, i.y - 15)
    lr.AddPoint(i.x + 45, i.y -45)
    lr.AddPoint(i.x + 15, i.y -45)
    lr.AddPoint(i.x + 15, i.y - 15)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(lr)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 6)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 6)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #lm
    lm = ogr.Geometry(ogr.wkbLinearRing)
    lm.AddPoint(i.x - 15, i.y - 15)
    lm.AddPoint(i.x + 15, i.y - 15)
    lm.AddPoint(i.x + 15, i.y -45)
    lm.AddPoint(i.x - 15, i.y -45)
    lm.AddPoint(i.x - 15, i.y - 15)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(lm)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 7)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 7)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #ll
    ll = ogr.Geometry(ogr.wkbLinearRing)
    ll.AddPoint(i.x - 45, i.y - 45)
    ll.AddPoint(i.x - 45, i.y - 15)
    ll.AddPoint(i.x - 15, i.y - 15)
    ll.AddPoint(i.x - 15, i.y -45)
    ll.AddPoint(i.x - 45, i.y - 45)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ll)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 8)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 8)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)
    #le
    le = ogr.Geometry(ogr.wkbLinearRing)
    le.AddPoint(i.x - 45, i.y + 15)
    le.AddPoint(i.x - 15, i.y + 15)
    le.AddPoint(i.x - 15, i.y - 15)
    le.AddPoint(i.x - 45, i.y - 15)
    le.AddPoint(i.x - 45, i.y + 15)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(le)
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(polygon)
    feature.SetField("point_ID", index)
    feature.SetField("polygon_ID", 9)
    feature.SetField("PA_name", str(PA))
    layer.CreateFeature(feature)

    featkml = ogr.Feature(defnkml)
    featkml.SetGeometry(polygon)
    featkml.SetField("point_ID", index)
    featkml.SetField("polygon_ID", 9)
    featkml.SetField("PA_name", str(PA))
    layerkml.CreateFeature(featkml)

shapefile = None
data_sourcekml = None
print (Name_list)

# end time count
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")