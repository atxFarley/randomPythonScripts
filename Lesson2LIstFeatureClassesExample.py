# Copies all feature classes from one folder to another
import arcpy
 
try:
    arcpy.env.workspace = "C:/PSUGIS/Geog485/Lesson1/Lesson1"
 
    # List the feature classes in the Lesson 1 folder
    fcList = arcpy.ListFeatureClasses()
 
    # Loop through the list and copy the feature classes to the Lesson 2 PracticeData folder
    for featureClass in fcList:
        arcpy.CopyFeatures_management(featureClass, "C:/PSUGIS/Geog485/Lesson2/PracticeData/" + featureClass)
 
except:
    print "Script failed to complete"
    print arcpy.GetMessages(2)