import arcpy

featureClass = arcpy.GetParameterAsText(0)

desc = arcpy.Describe(featureClass)

print "Data Type: " + desc.dataType

print "Shape Type: " + desc.shapeType

