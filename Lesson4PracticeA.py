import csv
import Lesson4APracticeModule
import arcpy
from arcpy import env


# Set workspace
env.workspace = r"C:\PSUGIS\GEOG485\Lesson4"
env.overwriteOutput = True

# Set up input and output variables for the script
mysteryStateFile = open( r"C:\PSUGIS\GEOG485\Lesson4\Lesson4PracticeExercises\Lesson4PracticeExerciseA\MysteryStatePoints.txt", "rU")
polygonFC =  r"C:\PSUGIS\GEOG485\Lesson4\Lesson4PracticeExercises\Lesson4PracticeExerciseA\MysteryState.shp"
spatialRef = arcpy.Describe(polygonFC).spatialReference


# Set up CSV reader and process the header
csvReader = csv.reader(mysteryStateFile)
latIndex = 1
lonIndex = 0

# Create an empty array object
vertexArray = arcpy.Array()

# Loop through the lines in the file and get each coordinate
for row in csvReader:
    lat = row[latIndex]
    lon = row[lonIndex]
 
    # Make a point from the coordinate and add it to the array
    vertex = arcpy.Point(lon,lat)
    vertexArray.add(vertex)

# Write the array to the feature class as a polyline feature
Lesson4APracticeModule.addPolygon(vertexArray, spatialRef, polygonFC)