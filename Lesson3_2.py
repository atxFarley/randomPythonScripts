import arcpy
 
arcpy.env.workspace = "C:\\PSUGIS\\GEOG485\\Lesson3\\USA.gdb"
featureClassList = arcpy.ListFeatureClasses()
clipFeature = "C:\\PSUGIS\\GEOG485\\Lesson3\\Alabama.gdb\\StateBoundary"
 
for featureClass in featureClassList:
    arcpy.Clip_analysis(featureClass, clipFeature, "C:\\PSUGIS\\GEOG485\\Lesson3\\Alabama.gdb\\" + featureClass)
