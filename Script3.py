# Opens a feature class from a geodatabase and prints the spatial reference
 
import arcpy
 
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\suitable_land.shp"
 
# Describe the feature class and get its spatial reference   
desc = arcpy.Describe(featureClass)
# Print the Data Type
print "Data Type: " + desc.dataType
#Print the children of this Descbribe ojbect
print("Children:")

for child in desc.children:
    print child.name
    

spatialRef = desc.spatialReference

# Print the spatial reference name
print spatialRef.Name