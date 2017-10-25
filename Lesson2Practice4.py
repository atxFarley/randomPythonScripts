import arcpy


inputPath = "C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\"
inputFeatureClass = "Precip2008Readings.shp"
outPath = "C:\\PSUGIS\\GEOG485\\Lesson2\\PracticeData\\"
#This needs to happen for the CreateFeatures tool
env.workspace = outPath
geometry_type = "POINT"
template = "Precip2008Readings.shp"
has_m = "DISABLED"
has_z = "DISABLED"


# Use Describe to get a SpatialReference object
spatial_reference = arcpy.Describe("C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\Precip2008Readings.shp").spatialReference


for year in range(2009, 2013):
    outname = "Precip"+str(year)+"Readings.shp"
    # Execute CreateFeatureclass
    #arcpy.CreateFeatureclass_management(outPath, outname, geometry_type, template, has_m, has_z, spatial_reference)
    arcpy.CreateFeatureclass_management(outPath, outname, geometry_type, template, has_m, has_z, template)
    print arcpy.GetMessages()
    







    