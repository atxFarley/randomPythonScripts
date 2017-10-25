#This script reprojects vector datasets in a directory
#supplied as an input parameter.  
#The target projection is also supplied as an input parameter

#Import only the required modules from the ArcPy site package
import os, time
import arcpy
from arcpy import env
from arcpy.da import *

#Override environment variables
#allow output to be overwritten
#for the sake of this assignment
arcpy.env.overwriteOutput = True

#Specify target folder and target projection
targetFolder = arcpy.GetParameterAsText(0)
targetProjectionDataset = arcpy.GetParameterAsText(1)

arcpy.AddMessage("Executing: {0} {1}".format(targetFolder, targetProjectionDataset))
arcpy.AddMessage("Running Script to Batch Reproject")

#target folder exists
boolTargetFolderExists  = False

#target projection dataset exists
boolTargetProjectionExists = False

#Reprojected Datasets
listReprojected = []

#Skipped Datasets
listSkipped = []

#License Availability boolean
boolProductLicensAvail = True
#strProductCheckReturn = ""
#License/Product Check Only necessary when running outside of an ArcMap script tool
#try:
    #Check for license availability before attempting anything else
    #Project tool available on ArcGIS Desktop Basic
    #strProductCheckReturn1 = arcpy.CheckProduct("arcview")
    #strProductCheckReturn2 = arcpy.CheckProduct("arceditor")
    #strProductCheckReturn3 = arcpy.CheckProduct("arcinfo")      
    #if ( (strProductCheckReturn1 == "Available") or (strProductCheckReturn2 == "Available") or (strProductCheckReturn3 == "Available")):
        #boolProductLicensAvail = True
        #arcpy.AddMessage("License Available")
#except Exception as e:
    #arcpy.AddError("Exception caught checking license availability")

#Now check for existence of target folder
try:
    boolTargetFolderExists  = os.path.exists(targetFolder)
    arcpy.AddMessage("Target Folder {0} Exists = {1} ".format(targetFolder, str(boolTargetFolderExists)))
except Exception as e:
    arcpy.AddError("Exception caught checking for target folder existence")

#The workspace environment must be set first before using several of the List functions,
#including ListDatasets
arcpy.env.workspace = targetFolder

#Now check for existence of target projection dataset
try:
    boolTargetProjectionExists = arcpy.Exists(targetProjectionDataset)
    arcpy.AddMessage("Target Projection Dataset {0} Exists = {1} ".format(targetProjectionDataset, str(boolTargetProjectionExists)))
except Exception as e:
    arcpy.AddError("Exception caught checking for target projection dataset existence")

#If license is available and target folder and target projection dataset exists, 
#okay to proceed

if(boolProductLicensAvail and  boolTargetFolderExists and boolTargetProjectionExists):
    #Get target Spatial Reference before proceeding
    arcpy.AddMessage("Proceeding the Reprojection")
    spatialRefName = ""
    try:
        #Use the ArcPy Describe function to obtain the Spatial Reference object
        targetSpatialRef = arcpy.Describe(targetProjectionDataset).spatialReference
        spatialRefName = targetSpatialRef.name
        arcpy.AddMessage("Target Spatial Referenence {0}".format(spatialRefName))
    except:
        arcpy.AddError("Cannot obtain Spatial Reference of target projection dataset")

    #If we have a spatial reference, proceed
    if (spatialRefName != "" and spatialRefName != "Unknown"):
        #Get the target datasets
        #uses the environment workspace set above
        #datasetList = arcpy.ListDatasets()
        datasetList = arcpy.ListFeatureClasses()        
        arcpy.AddMessage("Datasets found  = {0}".format(str(len(datasetList))))
        #Loop through each dataset list
        for dataset in datasetList:
            #Compare the spatial reference of the dataset to the target spatial reference
            datasetSpatialRef  = arcpy.Describe(dataset).spatialReference
            datasetSpatialRefName  = datasetSpatialRef.name
            arcpy.AddMessage("Dataset Spatial Reference {0}".format(datasetSpatialRefName))
             #only proceed wtih reprojection if not already in target projection
            if (datasetSpatialRefName != spatialRefName):
                #create the target projected dataset name from original dataset
                #obtain rootname before file extension
                strTargetName = ""               
                try:
                    dotIndex = dataset.find(".")
                    if(dotIndex > 0):
                        targetRootName = dataset[:dotIndex]
                        strTargetName = targetRootName + "_projected" +  dataset[dotIndex:]
                    else:
                        strTargetName  += "_projected" 
                    arcpy.AddMessage("Target name: " + strTargetName)
                except Exception as e:
                    #set strTargetName back to empty string and stop processing
                    strTargetName = ""
                    arcpy.AddError("Exception caught formatting target name")
                   
                #Proceed is target name is not empty
                if (strTargetName != ""):
                    try:
                        fullTargetLocation = os.path.join(targetFolder, strTargetName)
                        #print "Full Target Location {0}".format(fullTargetLocation)
                        #Call the Project Tool
                        arcpy.AddMessage("Calling Project tool for input dataset {0} with target location {1} in output coordinate system {2}".format(dataset, fullTargetLocation, spatialRefName))
                        result  = arcpy.Project_management(dataset, fullTargetLocation, targetSpatialRef)                       
                        arcpy.AddMessage(result.getMessages())
                        listReprojected.append(dataset)
                    except:
                        #On exception add error and messages 
                        arcpy.AddError("Exception caught with Project Tool")        
                else:
                    arcpy.AddError("Unable to Reproject {0} because target name could not be set".format(dataset))                   
            else:
                listSkipped.append(dataset)
                arcpy.AddMessage("Skipping {0}.  Already in target projection.".format(dataset))                
    else:
        arcpy.AddError("Unable to reproject because spatial reference could not be obtained from target dataset {0}".fomat(targetProjectionDataset))
else:
    arcpy.AddError("Unable to complete reprojection:  License availability =  " + str(boolProductLicensAvail) + ", Target Folder Existence = " + str(boolTargetFolderExists) + ", Target Projection Dataset Existence = " + str(boolTargetProjectionExists))

customMessage = "Projected "
s = ", "
customMessage  += s.join(listReprojected)
arcpy.AddMessage(customMessage)
arcpy.AddMessage("Completed Batch Reproject Script")

                        

