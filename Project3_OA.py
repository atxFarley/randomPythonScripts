#This script takes two input feature classes
#extracts each distint amenity for each country
#and creates shapefiles for each amenity within that country

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
print "Executing for target workspace: {0}, input amenities feature class: {1}, input countries feature class: {2}, amenities source {3}".format(targetWorkspace,inputAmenitiesFeatureClass, inputCountriesFeatureClass, amenitySource )
#arcpy.AddMessage("Running Script to Extract amenities")
#arcpy.AddMessage("Executing for target workspace: {0}, input amenities feature class: {1}, input countries feature class: {2}, target country: {3}, amenities: {4}, amenities source {5}".format(targetWorkspace,inputAmenitiesFeatureClass, inputCountriesFeatureClass,  amenitySource ))

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

    #obtain list of distict amenities and create a temporary feature layer for each.  
    targetAmenitiesList = []
    #"amenity" IS NOT NULL AND "amenity" <> ''
    amenitySearchWhereClause = '"' + str(amenityNameField) + '" IS NOT NULL'
    try:
        with arcpy.da.SearchCursor(inputAmenitiesFeatureClass, (amenityNameField, ), where_clause=amenitySearchWhereClause) as cursor:
            for row in cursor:
                distinctAmenity= row[0]
                stippedAmenity  = distinctAmenity.lstrip().rstrip()
                if (stippedAmenity != ""):
                    if (distinctAmenity not in targetAmenitiesList):
                        targetAmenitiesList.append(distinctAmenity)
                        print "Added amenity {0} to list".format(distinctAmenity)
                        arcpy.AddMessage("Added amenity {0} to list".format(distinctAmenity))
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except:
        print "Exception caught in SearchCursor obtaining distinct amenities"
        #arcpy.AddError("Exception caught in SearchCursor obtaining distinct amenities")

    #create temporary amenity layers    
    amenityLayerList = []
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
        try:
            arcpy.MakeFeatureLayer_management(inputAmenitiesFeatureClass, amenityLayerName,  amenityLayerWhereClause)
            amenityLayerList.append(amenityLayerName);
            print "Amenity Feature Layer created {0}".format(amenityLayerName)
            #arcpy.AddMessage("Amenity Feature Layer created {0}".format(amenityLayerName))
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)
        except:
            print "General Exception caught making amenity feature layer"
            #arcpy.AddError("General Exception caught making amenity feature layer")

    #obtain list of countries and create temporary layers for each
    countriesList = []
    countrySearchWhereClause = '"' + str(countryNameField) + '" IS NOT NULL'
    try:
        with arcpy.da.SearchCursor(inputCountriesFeatureClass, (countryNameField, ),  where_clause=countrySearchWhereClause) as cursor:
            for row in cursor:
                distinctCountry = row[0]
                if (distinctCountry not in countriesList):
                    countriesList.append(distinctCountry)
                    print "Added country {0} to list".format(distinctCountry)
                    arcpy.AddMessage("Added country {0} to list".format(distinctCountry))
    except arcpy.ExecuteError:
        print arcpy.GetMessages(2)
    except:
        print "Exception caught in SearchCursor obtaining countries list"
        #arcpy.AddError("Exception caught in SearchCursor obtaining countries list")

    #create temporary country layers    
    countryLayersList= []    
    for targetCountry in countriesList:
            #Make a feature layer of the target country from the countries input feature class
            countriesLayerWhereClause =  whereClause = '"' + str(countryNameField) + '" = '+"'"+str(targetCountry) + "'"
            countryLayerName = str(targetCountry).replace(" ", "") + "Layer"
            try:
                arcpy.MakeFeatureLayer_management(inputCountriesFeatureClass, countryLayerName, countriesLayerWhereClause)
                countryLayersList.append(countryLayerName)
                print "Country Feature Layer created {0}".format(countryLayerName)
                #arcpy.AddMessage("Country Feature Layer created {0}".format(countryLayerName))
            except arcpy.ExecuteError:
                print arcpy.GetMessages(2)
            except:
                print "General Exception caught making target country feature layer"
                #arcpy.AddError("General Exception caught making target country feature layer")
    try:
        if ((len(countryLayersList) > 0) and (len(amenityLayerList) > 0)):   
            #Iterate through the amenity layers 
            for amenityLayerName in amenityLayerList:
                #Iterate through country layers list
                for countryLayerName in countryLayersList:
                    try:
                        #SelectLayerByLocation
                        arcpy.SelectLayerByLocation_management(amenityLayerName,"COMPLETELY_WITHIN",countryLayerName)

                        #Save the feature layer to a feature class only if there are records
                        selectResult = arcpy.GetCount_management(amenityLayerName)
                        resultCount = int(selectResult.getOutput(0))

                        if (resultCount > 0):
                            outputFeatureClass = str(countryLayerName).replace("Layer", "") + amenityLayerName.replace("Layer", "")
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
                        else:
                            print "SelectLayerByLocation found zero amenity {0} points in country {1}, no feature class created.".format(amenityLayerName.replace("Layer", ""),  str(countryLayerName).replace("Layer", ""))
                            #arcpy.AddMessage("SelectLayerByLocation found zero amenity {0} points in country {1}, no feature class created.".format(amenityLayerName.replace("Layer", ""),  str(countryLayerName).replace("Layer", "")))
                    except arcpy.ExecuteError:
                        print arcpy.GetMessages(2)
                    except:
                        print "General Exception caught making amenity feature layer"
                        #arcpy.AddError("General Exception caught making amenity feature layer")                 

    finally:
        #Delete all the temporary layers
        for amenityLayerName in amenityLayerList:
            arcpy.Delete_management(amenityLayerName)
            print "Temporarty Amenity Feature Layer deteled {0}".format(amenityLayerName)
            #arcpy.AddMessage("Temporarty Amenity Feature Layer deteled {0}".format(amenityLayerName))

        for countryLayerName in countryLayersList:
            arcpy.Delete_management(countryLayerName)
            print "Temporarty Country Feature Layer deteled {0}".format(countryLayerName)
            #arcpy.AddMessage("Temporarty Country Feature Layer deteled {0}".format(countryLayerName))

else:
    print "Unable to complete amenities extraction:  License availability =  " + str(boolProductLicensAvail) + ", Workspace Existence = " + str(boolTargetWorkspaceExists) + ", Input Amenities = " + str(boolInputAmenitiesExist) + ", Input Countries = " + str(boolInputCountriesExist)
    #arcpy.AddError("Unable to complete amenities extraction:  License availability =  " + str(boolProductLicensAvail) + ", Workspace Existence = " + str(boolTargetWorkspaceExists) + ", Input Amenities = " + str(boolInputAmenitiesExist) + ", Input Countries = " + str(boolInputCountriesExist))

print "Completed Amenities Extraction"
#arcpy.AddMessage("Completed Amenities Extraction")

                        

