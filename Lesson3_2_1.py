# Reads the fields in a feature class
 
import arcpy
 
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson3\\USA.gdb\Cities"
fieldList = arcpy.ListFields(featureClass)
# Loop through each field in the list and print the name
for field in fieldList:
    print field.name