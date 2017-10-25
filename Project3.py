#This script extracts amenities from a shapefile for a specific country
#then creates a separate shapefile for each amenity
#each new shapefile contains a source field to indicate the origin of the data

#Import only the required modules from the ArcPy site package
import os, time
import arcpy
from arcpy import env
from arcpy.da import *

#Override environment variables
#allow output to be overwritten
#for the sake of this assignment
arcpy.env.overwriteOutput = True

#Specify input parameters
targetWorkspace = r"C:\PSUGIS\GEOG485\Lesson3\Project3"
#targetWorkspace = arcpy.GetParameterAsText(0)
inputAmenitiesFeatureClass = r"OSMpoints.shp"
#inputAmenitiesFeatureClass = arcpy.GetParameterAsText(1)
inputCountriesFeatureClass = r"CentralAmerica.shp"
#inputCountriesFeatureClass = arcpy.GetParameterAsText(2)
targetCountry = "El Salvador"
#targetCountry = arcpy.GetParameterAsText(3)
targetAmenitiesList = ["school", "hospital", "place_of_worship"]
#targetAmenitiesList = arcpy.GetParameterAsText(4)
amenitySource = "OpenStreetMap"
#amenitySource = arcpy.GetParameterAsText(5)

#Specifify additional variables needed within the script
countryNameField = "NAME" #This could also be an input parameter, would need to add validation using arcpy.ListFields(inputCountriesFeatureClass)
amenityNameField = "amenity" #This could also be an input parameter,  would need to add validation using arcpy.ListFields(inputAmenitiesFeatureClass)
sourceFieldName = "source"
commaDelimiter = ", "
outputDataType = ""

#Add some messaging
print "Running Script to Extract amenities"
print "Executing for target workspace: {0}, input amenities feature class: {1}, input countries feature class: {2}, target country: {3}, amenities: {4}, amenities source {5}".format(targetWorkspace,inputAmenitiesFeatureClass, inputCountriesFeatureClass, targetCountry, commaDelimiter.join(targetAmenitiesList), amenitySource )
#arcpy.AddMessage("Running Script to Extract amenities")
#arcpy.AddMessage("Executing for target workspace: {0}, input amenities feature class: {1}, input countries feature class: {2}, target country: {3}, amenities: {4}, amenities source {5}".format(targetWorkspace,inputAmenitiesFeatureClass, inputCountriesFeatureClass, targetCountry, commaDelimiter.join(targetAmenitiesList), amenitySource ))

#Perform validation for the standalone script
#target workspace and input feature classes exist
boolTargetWorkspaceExists  = False
boolInputAmenitiesExist = False
boolInputCountriesExist = False

#License Availability boolean
boolProductLicensAvail = True
strProductCheckReturn = ""
#License/Product Check Only necessary when running outside of an ArcMap script tool
try:
    #Check for license availability before attempting anything else
    #Project tool available on ArcGIS Desktop Basic
    strProductCheckReturn1 = arcpy.CheckProduct("arcview")
    strProductCheckReturn2 = arcpy.CheckProduct("arceditor")
    strProductCheckReturn3 = arcpy.CheckProduct("arcinfo")      
    if ( (strProductCheckReturn1 == "Available") or (strProductCheckReturn2 == "Available") or (strProductCheckReturn3 == "Available")):
        boolProductLicensAvail = True
        print "License Available"
        #arcpy.AddMessage("License Available")
except Exception as e:
    print "Exception caught checking license availability"
    #arcpy.AddError("Exception caught checking license availability")

#Now check for existence of target workspace
try:
    boolTargetWorkspaceExists  = os.path.exists(targetWorkspace)
    #Once workspace existence is verified, set the environment workspace
    arcpy.env.workspace = targetWorkspace
    print "Target Folder {0} Exists = {1} ".format(targetWorkspace, str(boolTargetWorkspaceExists))
    #arcpy.AddMessage("Target Folder {0} Exists = {1} ".format(targetWorkspace, str(boolTargetWorkspaceExists)))
except Exception as e:
    print "Exception caught checking for target workspace existence"
    #arcpy.AddError("Exception caught checking for target workspace existence")


#Now check for existence of input feature classes
try:
    boolInputAmenitiesExist = arcpy.Exists(inputAmenitiesFeatureClass)
    boolInputCountriesExist = arcpy.Exists(inputCountriesFeatureClass)
    print "Input Feature Class {0} Exists = {1} ".format(inputAmenitiesFeatureClass, str(boolInputAmenitiesExist))
    #arcpy.AddMessage("Input Feature Class {0} Exists = {1} ".format(inputAmenitiesFeatureClass, str(boolInputAmenitiesExist)))
    print "Input Feature Class {0} Exists = {1} ".format(inputCountriesFeatureClass, str(boolInputCountriesExist))
    #arcpy.AddMessage("Input Feature Class {0} Exists = {1} ".format(inputAmenitiesFeatureClass, str(boolInputAmenitiesExist)))

    #Determine what the output data type will be for later in the script
    descInputAmenitites = arcpy.Describe(inputAmenitiesFeatureClass)
    outputDataType = descInputAmenitites.dataType
    print "Output Feature Class Data Type {0}".format(outputDataType)
    #arcpy.AddMessage("Output Feature Class Data Type {0}".format(outputDataType))
except Exception as e:
    print "Exception caught checking for input feature classes existence"
    arcpy.AddError("Exception caught checking for input feature classes existence")

#If license is available and target workspace and input features exist 
#okay to proceed

if(boolProductLicensAvail and  boolTargetWorkspaceExists and boolInputAmenitiesExist and boolInputCountriesExist):
    print "Validation complete, proceeding with amenities extraction"
    #arcpy.AddMessage("Validation complete, proceeding with amenities extraction")

    #Make a feature layer of the target country from the countries input feature class
    countriesLayerWhereClause =  whereClause = '"' + str(countryNameField) + '" = '+"'"+str(targetCountry) + "'"
    countryLayerName = str(targetCountry).replace(" ", "") + "Layer"
    boolCountryLayerCreated = False
    try:
        arcpy.MakeFeatureLayer_management(inputCountriesFeatureClass, countryLayerName, countriesLayerWhereClause)
        boolCountryLayerCreated = True
        print "Country Feature Layer created {0}".format(countryLayerName)
        #arcpy.AddMessage("Country Feature Layer created {0}".format(countryLayerName))
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except:
        print "General Exception caught making target country feature layer"
        #arcpy.AddError("General Exception caught making target country feature layer")

    if (boolCountryLayerCreated):
        for amenity in targetAmenitiesList:
            print "Amenity: " + amenity
            #arcpy.AddMessage( "Amenity: " + amenity)
            #Make a temporary feature layer for each amenity
            amenityLayerWhereClause =  whereClause = '"' + str(amenityNameField) + '" = '+"'"+str(amenity) + "'"
            amenityString = str(amenity).title()
            amenityString = amenityString.replace("_", "")
            amenityString = amenityString.replace(" ", "")
            amenityString = amenityString.replace(".", "")
            amenityLayerName = amenityString+"Layer"
            amenityLayerName = str(targetCountry).replace(" ", "") +  amenityLayerName
            boolAmenityLayerCreated = False
            try:
                arcpy.MakeFeatureLayer_management(inputAmenitiesFeatureClass, amenityLayerName,  amenityLayerWhereClause)
                boolAmenityLayerCreated = True
                print "Amenity Feature Layer created {0}".format(amenityLayerName)
                #arcpy.AddMessage("Amenity Feature Layer created {0}".format(amenityLayerName))
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except:
                print "General Exception caught making amenity feature layer"
                #arcpy.AddError("General Exception caught making amenity feature layer")

            if (boolAmenityLayerCreated):
                try:
                    #Select those amenities in target country
                    arcpy.SelectLayerByLocation_management(amenityLayerName,"COMPLETELY_WITHIN",countryLayerName)

                    #Save the feature layer to a feature class
                    outputFeatureClass = amenityLayerName.replace("Layer", "")
                    arcpy.CopyFeatures_management(amenityLayerName, outputFeatureClass)

                    #set full feature class name based on data type
                    if("ShapeFile" == outputDataType):
                        outputFeatureClass  +=".shp"
  
                    #Add field to the new feature class
                    fieldLength=25
                    arcpy.AddField_management(outputFeatureClass, sourceFieldName, "TEXT",field_length=fieldLength, field_is_nullable="NULLABLE")
                
                    #Iterate each record in new feature class and update the new field
                    #obtain Update Cursor to iterate through the new amenities feature class
                    with arcpy.da.UpdateCursor (outputFeatureClass, (sourceFieldName,)) as cursor:
                        for row in cursor:
                            row[0] = amenitySource
                            cursor.updateRow(row)
    
                except arcpy.ExecuteError:
                    print arcpy.GetMessages(2)
                except:
                    print "General Exception caught making amenity feature layer"
                    #arcpy.AddError("General Exception caught making amenity feature layer")
                finally:
                    #Delete the temporary amenity layer
                    arcpy.Delete_management(amenityLayerName)                    
            else:
                print "Amenity Feature Layer was not created, Unable to continue"
                #arcpy.AddError("Amenity Feature Layer was not created, Unable to continue")  

        #Delete the country layer
        try:
            arcpy.Delete_management(countryLayerName)
            print "Temporarty Country Feature Layer deteled {0}".format(countryLayerName)
            #arcpy.AddMessage("Temporarty Country Feature Layer deteled {0}".format(countryLayerName))
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except:
            print "General Exception caught deleting country layer"
            #arcpy.AddError("General Exception caught deleting country layer")


    else:
        print "Country Feature Layer was not created, Unable to continue"
        #arcpy.AddError("Country Feature Layer was not created, Unable to continue")
else:
    print "Unable to complete amenities extraction:  License availability =  " + str(boolProductLicensAvail) + ", Workspace Existence = " + str(boolTargetWorkspaceExists) + ", Input Amenities = " + str(boolInputAmenitiesExist) + ", Input Countries = " + str(boolInputCountriesExist)
    #arcpy.AddError("Unable to complete amenities extraction:  License availability =  " + str(boolProductLicensAvail) + ", Workspace Existence = " + str(boolTargetWorkspaceExists) + ", Input Amenities = " + str(boolInputAmenitiesExist) + ", Input Countries = " + str(boolInputCountriesExist))

print "Completed Amenities Extraction"
#arcpy.AddMessage("Completed Amenities Extraction")

                        

