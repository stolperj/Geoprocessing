#imports
import os
from collections import Counter
import time
import ogr
#import baumiTools as bt

#start time count
starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("Starting process, time: " + starttime)
print("")

#Exercise 1 - sanity check
filenames = os.listdir("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/")  # get all files' and folders' names in the current directory
print (filenames)
len(filenames)

# How many scenes from individual sensor per footprint?
filenames230078 = os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/230_078/")
print (filenames230078)
#set individual master lists
LC8_list = ['LC08']
sum(any(m in L for m in LC8_list) for L in filenames230078)
LE7_list = ['LE07']
sum(any(m in L for m in LE7_list) for L in filenames230078)
LT5_list = ['LT05']
sum(any(m in L for m in LT5_list) for L in filenames230078)
LT4_list = ['LT04']
sum(any(m in L for m in LT4_list) for L in filenames230078)

filenames230079= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/230_079/")
print (filenames230079)
sum(any(m in L for m in LC8_list) for L in filenames230079)
sum(any(m in L for m in LE7_list) for L in filenames230079)
sum(any(m in L for m in LT5_list) for L in filenames230079)
sum(any(m in L for m in LT4_list) for L in filenames230079)

filenames230077= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/230_077/")
print (filenames230077)
sum(any(m in L for m in LC8_list) for L in filenames230077)
sum(any(m in L for m in LE7_list) for L in filenames230077)
sum(any(m in L for m in LT5_list) for L in filenames230077)
sum(any(m in L for m in LT4_list) for L in filenames230077)

filenames229077= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/229_077/")
print (filenames229077)
sum(any(m in L for m in LC8_list) for L in filenames229077)
sum(any(m in L for m in LE7_list) for L in filenames229077)
sum(any(m in L for m in LT5_list) for L in filenames229077)
sum(any(m in L for m in LT4_list) for L in filenames229077)

filenames229079= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/229_079/")
print (filenames229079)
sum(any(m in L for m in LC8_list) for L in filenames229079)
sum(any(m in L for m in LE7_list) for L in filenames229079)
sum(any(m in L for m in LT5_list) for L in filenames229079)
sum(any(m in L for m in LT4_list) for L in filenames229079)

filenames228079= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/228_079/")
print (filenames228079)
sum(any(m in L for m in LC8_list) for L in filenames228079)
sum(any(m in L for m in LE7_list) for L in filenames228079)
sum(any(m in L for m in LT5_list) for L in filenames228079)
sum(any(m in L for m in LT4_list) for L in filenames228079)

filenames228077= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/228_077/")
print (filenames228077)
sum(any(m in L for m in LC8_list) for L in filenames228077)
sum(any(m in L for m in LE7_list) for L in filenames228077)
sum(any(m in L for m in LT5_list) for L in filenames228077)
sum(any(m in L for m in LT4_list) for L in filenames228077)

filenames229078= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/229_078/")
print (filenames229078)
sum(any(m in L for m in LC8_list) for L in filenames229078)
sum(any(m in L for m in LE7_list) for L in filenames229078)
sum(any(m in L for m in LT5_list) for L in filenames229078)
sum(any(m in L for m in LT4_list) for L in filenames229078)

filenames228078= os.listdir ("/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/228_078/")
print (filenames228078)
sum(any(m in L for m in LC8_list) for L in filenames228078)
sum(any(m in L for m in LE7_list) for L in filenames228078)
sum(any(m in L for m in LT5_list) for L in filenames228078)
sum(any(m in L for m in LT4_list) for L in filenames228078)

#count the number of scenes that do not have the “correct” number of files in them and generate a text-file, in which each corrupt scene
corrupt_list = []

import os
path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/230_078/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/230_079/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/230_077/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/229_077/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/229_079/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/228_079/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/228_077/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/229_078/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)

path = "/Users/juliastolper/Downloads/Assignment01_data/Part01_Landsat/228_078/"
cor = 19
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LC08" or "LE07")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != cor: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
corx = 21
folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name)) and name.startswith("LT04" or "LT05")]) # get all directories
for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) != corx: # if smaller than the limit, print folder and number of contents
        print(folder,len(contents))
        corrupt_list.append(folder)
len(corrupt_list)
# open a (new) file to write
outF = open("corrupt.txt", "w")
outF.writelines(corrupt_list)
outF.close()

#Exercise 2 - data overview

#number of shapefiles and rasterfiles

ex2 = os.listdir("/Users/juliastolper/Downloads/Assignment01_data/Part02_GIS-Files/")  # get all files' and folders' names in the current directory
print (ex2)
len(ex2)

#shapefiles
shp_list=[]
for entry in ex2:
    if entry.endswith(".shp"):
        print(entry)
        shp_list.append(entry)
len(shp_list)
#rasterfiles
ras_list=[]
for entry in ex2:
    if entry.endswith(".tif"):
        print(entry)
        ras_list.append(entry)
len(ras_list)

#identify missing shapefile information
len(shp_list)
print(shp_list)
shpnew=[]
for word in shp_list:
    word=word[:-4]
    shpnew.append(word)
print (shpnew)

dbf_list=[]
for entry in ex2:
    if entry.endswith(".dbf"):
        print(entry)
        dbf_list.append(entry)
len(dbf_list)
print(dbf_list)
dbfnew=[]
for word in dbf_list:
    word=word[:-4]
    dbfnew.append(word)
print (dbfnew)

prj_list=[]
for entry in ex2:
    if entry.endswith(".prj"):
        print(entry)
        prj_list.append(entry)
len(prj_list)
print(prj_list)

len(dbf_list)
print(dbf_list)
prjnew=[]
for word in prj_list:
    word=word[:-4]
    prjnew.append(word)
print (prjnew)

returnMatches(shpnew, dbfnew)

dbfcomplete=set(shpnew).intersection(dbfnew)
prjcomplete=set(shpnew).intersection(prjnew)
shapecomplete=set(dbfcomplete).intersection(prjcomplete)
shapeincomplete=set(shpnew)-shapecomplete
print(shapeincomplete)
len(shapeincomplete)
list(shapeincomplete)
shapeincomplete

# open a (new) file to write
outF = open("shapeincomplete.txt", "w")
outF.writelines(shapeincomplete)
outF.close()

#end time count
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")