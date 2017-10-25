#Module that contains common geoprocessing tasks

#Create a feature class
def createFeatureClass(outputPath, outputFCName, geometryType, template, hasM, hasZ, spatialRef):
    import arcpy
    import commonValidation
    try:
        if (commonValidation.workspaceExists(outputPath)):
            # Execute CreateFeatureclass
            arcpy.CreateFeatureclass_management(outputPath, outputFCName,geometryType, template, hasM, hasZ, spatialRef)
            print "Feature Class {0} created".format(outputFCName)
            #arcpy.AddMessage(print "Feature Class {0} created".format(outputFCName))
        else:
            print "Output Path does not exist {0}".format(outputPath)
            #arcpy.AddError ("Output Path does not exist {0}".format(outputPath))
    except Exception as e: 
          print "Exception caught creating feature class {0}".format(e.args[0])
            #arcpy.AddError ("Exception caught creating feature class {0}".format(e.args[0]))

#Add field to a feature class
def addFieldToFeatureClass(featureClass, inputTable, fieldName, fieldType, fieldLength, fieldNullable):
    import arcpy
    import commonValidation
    try:
        if (commonValidation.featureClassExists(featureClass) and commonValidation.featureClassTableExists(featureClass, inputTable)):        
            # Add field to Feature class table
            arcpy.AddField_management(inputTable, fieldName, fieldType,field_length=fieldLength, field_is_nullable=fieldNullable)                     
            print "Field Added to input table{0} of feature class {1}".format(inputTable, featureClass)
            #arcpy.AddMessage(print "Field Added to input table{0} of feature class {1}".format(inputTable, featureClass))
        else:
            print "Feature Class and/or feature class table does not exist {0} : {1}".format(featureClass, inputTable)
            #arcpy.AddError ("Feature Class does not exist {0}".format(featureClass))
    except Exception as e: 
        print "Exception caught adding field to feature class {0}".format(e.args[0])
        #arcpy.AddError ("Exception caught adding field to feature class {0}".format(e.args[0]))

                           