#This script creates vector contour lines from an input raster elevation dataset
#Uses default values of 25 meters for contour intervals and 0 for base contour

#Import only the required modules from the ArcPy site package
import arcpy
from arcpy import env
from arcpy.sa import *

#Override environment variables
#allow output to be overwritten
#since we are hard-coding output file
arcpy.env.overwriteOutput = True

#Specify default values
#contour interval should be 25 meters
intContourInterval = 25
#base contour should be 0
intBaseContour = 0

#Specify input and output rasters from parameters
#rasterInput = arcpy.GetParameterAsText(0)
#featClassOutput = arcpy.GetParameterAsText(1)

#Specify input and output as hardcoded-values
rasterInput = "C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\foxlake"
featClassOutput = "C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\foxlake_contours"
#z factor not required since native units of inputRaster are in meters already, so default value of 1
floatZFactor = 1

#For more robust exception handling
boolLicenseAvail = False
boolInputFileExists = False
strSpatialExtensionCheck = ""
#Super robust error checking and debugging on license check step (just because)
#Since CheckExtenstion and CheckOutExtension are ArcPy functions (not Tools),
#No Result object returned.  No Messages Produced
print "Begin Script"
try:
    #Check for license availability and check out upon availablity
    strSpatialExtensionCheck = arcpy.CheckExtension("spatial")
    print "SpatialExtensionCheck: " + strSpatialExtensionCheck
    if (strSpatialExtensionCheck == "Available"):
        arcpy.CheckOutExtension("spatial")
        boolLicenseAvail = True     
        print "Spatial license checked out"
    elif (strSpatialExtensionCheck == "Unavailable"):
        print "Spatial Extension License is not available"
    elif (strSpatialExtensionCheck == "NotLicensed"):
        print "Spatial Extension License not licensed"
    elif (strSpatialExtensionCheck == "Failed"):
        print "Spatial Extension Check Failed"
    else:
        print "Spatial Extension Check Returned something unexpected.  This should NEVER happen"
except:
    print "Exception caught checking out license"

#Now check for existence of input file
try:
    boolInputFileExists = arcpy.Exists(rasterInput)
    print "Raster Input File Exists: " + str(boolInputFileExists)
except:
    print "Exception caught checking for input file existence"

#If License check-out successful AND input file exists proceed to contouring task
#Contour is a Geoprocessing Tool, so this function will return a Result object and messages
if (boolLicenseAvail and boolInputFileExists):
    #Catch errors on Contour task
    try:
        #Create the contours
        print "Raster Input: " + str(rasterInput) + ", Feature Class Output: " + str(featClassOutput) + ", Contour Intervals (meters): " + str(intContourInterval) + ", Base Contour: " + str(intBaseContour)  + ", Z-Factor: " + str(floatZFactor)
        result = Contour(rasterInput, featClassOutput, intContourInterval, intBaseContour, floatZFactor)
        arcpy.AddMessage(result.GetMessages() )  
        print "Contour creation complete"      
    except:
        #On exception add error and messages 
        arcpy.AddError("Exception caught with Contour Tool")
        arcpy.AddMessage(arcpy.GetMessages() )
        print "Exceptin caught on Contour task"

    #Print Geoprocessing Tool Messages   
    print "Messages from all Geoprocessing Tools:"
    print "Error Messages: " + arcpy.GetMessages(2)
    print "Warning Messages: " + arcpy.GetMessages(1)
    print "Info Messages: " + arcpy.GetMessages(0)

    #Check the license back in regardless of contouring success
    #Catch errors on license check-in task
    try:
        arcpy.CheckInExtension("spatial")
        print "Spatial license checked back in"
    except:
        print "Exception caught checking in license"
else:
    print "Unable to run Geoprocessing Tool"
    print "spatial license availablity: " + str(boolLicenseAvail) + ", input file exists: " + str(boolInputFileExists)
     


print "End Script"


