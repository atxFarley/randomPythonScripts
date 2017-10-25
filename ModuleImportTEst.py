#This script reads a spreadhseet of
#observed rhino points and creates a polyline feature
#from the observed point coordinates
#for each unique rhino
#and inserts into a new feature class

#function to add the rhino point to the dictionary array value
def addRhinoPoint(map, rhino, lat, lon):
    print rhino
    point = arcpy.Point(lon, lat)
    if (rhino in map):
        print rhino + " in map already"        
        #pointArray = map[rhino]
        #pointArray.add(point)
        #map[rhino] = pointArray
        map[rhino].add(point)
    else:
        print "adding " + rhino + " to map"
        # Create an empty array object
        pointArray = arcpy.Array()
        pointArray.add(point)
        map[rhino] = pointArray


 
# Function to add a polyline
def addPolyline(cursor, nameFieldValue, pointArrayValue, spatialRef):
    if pointArrayValue.count > 0:
        polyline = arcpy.Polyline(pointArrayValue, spatialRef)
        cursor.insertRow((nameFieldValue, polyline))
        pointArrayValue.removeAll()


#Import the required modules from the ArcPy site package
import csv

import commonValidationTest
import commonGeoprocessingTest

#Override environment variables
#allow output to be overwritten
#for the sake of this assignment
arcpy.env.overwriteOutput = True

#Specify input parameters
targetWorkspace = r"C:\PSUGIS\GEOG485\Lesson4\Project4"
#targetWorkspace = arcpy.GetParameterAsText(0)
inputFile = r"C:\PSUGIS\GEOG485\Lesson4\Project4\RhinoObservations.csv"
#inputFile = arcpy.GetParameterAsText(1)
outputFeatureClass = r"RhinoTracking.shp"
#outputFeatureClass = arcpy.GetParameterAsText(2)

#Specifify additional variables needed within the script
#output feature class 
geometryType = "POLYLINE"
template = ""
hasM = "DISABLED"
hasZ = "DISABLED"
#Use coordinate system's factory code (or authority code)
#for WGS 1984 geographic coordinate system
#GCS_WGS_1984  = 4326
spatialRef = arcpy.SpatialReference(4326)
#feature class table field
rhinoNameField = "NAME"
fieldType = "TEXT"
fieldLength=25
fieldNullable="NON_NULLABLE"

#Add some messaging
print "Running Script to Create Rhino tracking feature class"
#arcpy.AddMessage("Running Script to Create Rhino tracking feature class")

#Perform validation for the standalone script
if(commonValidationTest.checkArcGISProduct() and  commonValidationTest.workspaceExists(targetWorkspace) and commonValidationTest.fileExists(inputFile)):
    print "Validation complete, proceeding creation of rhino tracking feature class"
    #arcpy.AddMessage("Validation complete, proceeding creation of rhino tracking feature class")

    #Once workspace existence is verified, set the environment workspace
    arcpy.env.workspace = targetWorkspace
    #Create the output feature class & addd rhino field name
    try:
        commonGeoprocessingTest.createFeatureClass(targetWorkspace, outputFeatureClass, geometryType, template, hasM, hasZ, spatialRef)
        commonGeoprocessingTest.addFieldToFeatureClass(outputFeatureClass, outputFeatureClass, rhinoNameField, fieldType, fieldLength, fieldNullable)
    except Exception as e:
        print "Exception caught in feature class creation {0}".format(e.args[0])
        #arcpy.AddError ("Exception caught in feature class creation {0}".format(e.args[0]))

    #If featureClass creation successful, continue to reading csv file and inserting rows
    if(commonValidationTest.featureClassExists(outputFeatureClass)):
        #Create the empty dictionary to store the rhino point array objects
        rhinoDict = {}
        #open the spreadsheet
        try:
            print "inputFile: " + inputFile
            csvFile = open(str(inputFile), "rU")
            csvReader = csv.reader(csvFile)
            header = csvReader.next()
            rhinoName = header.index("Rhino")
            lat = header.index("Y")
            lon = header.index("X")
            print "indexes  Rhino Name {0}, Latitude {1}, Longitude {2}".format(str(rhinoName), str(lat), str(lon)) 

            #Loop through the rows in the file, create POints and add to the rhino's Array    
            for row in csvReader:
                addRhinoPoint(rhinoDict, row[rhinoName], row[lat], row[lon])

            #Create the InsertCursor
            fieldNames = ("NAME", "SHAPE@")
            with arcpy.da.InsertCursor(outputFeatureClass, fieldNames) as cursor:
                #Now loop through the dictionary, create the Polyline and insert into feature class
                for key in rhinoDict.keys():
                    nameFieldValue = key
                    pointArrayValue  = rhinoDict[key]
                    addPolyline(cursor, nameFieldValue, pointArrayValue, spatialRef)
                   
        except Exception as e:
            print "Exception caught reading file {0}".format(e.args[0])
            #arcpy.AddError ("Exception caught reading file {0}".format(e.args[0]))


    else:
        print "Output Feature class {0} does not exist.  Unable to continue".format(outputFeatureClass)
        #arcpy.AddError("Output Feature class {0} does not exist.  Unable to continue".format(outputFeatureClass))        
else:
    print "Unable to complete creation of rhino tracking feature class:  License availability =  " + str(commonValidationTest.checkArcGISProduct()) + ", Workspace Existence = " + str(commonValidationTest.workspaceExists(targetWorkspace) ) + ", Input File = " + str(commonValidationTest.fileExists(inputFile))
    #arcpy.AddError("Unable to complete creation of rhino tracking feature class:  License availability =  " + str(commonValidationTest.checkArcGISProduct()) + ", Workspace Existence = " + str(commonValidationTest.workspaceExists(targetWorkspace) ) + ", Input File = " + str(commonValidationTest.fileExists(inputFile)))

print "Rhino Tracking Feature Class Creation script ended"
#arcpy.AddMessage("Rhino Tracking Feature Class Creation script ended")


