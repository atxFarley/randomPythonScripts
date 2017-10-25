import arcpy
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson3\\USA.gdb\\Cities"
desc = arcpy.Describe(featureClass)
spatialRef = desc.SpatialReference
print spatialRef.Name