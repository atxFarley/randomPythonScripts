# This script reads a GPS track in CSV format and
#  writes geometries from the list of coordinate pairs
import csv
import arcpy
from arcpy import env


# Set workspace
env.workspace = r"C:\PSUGIS\GEOG485\Lesson4"
env.overwriteOutput = True

# Set local variables
out_path = r"C:\PSUGIS\GEOG485\Lesson4"
out_name = "tracklines.shp"
geometry_type = "POLYLINE"
template = ""
has_m = "DISABLED"
has_z = "DISABLED"

# Use Describe to get a SpatialReference object
spatial_reference = arcpy.Describe(r"C:\PSUGIS\GEOG485\Lesson3\Project3\CentralAmerica.shp").spatialReference

# Execute CreateFeatureclass
arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, template, has_m, has_z, spatial_reference)
 
# Set up input and output variables for the script
gpsTrack = open(r"C:\PSUGIS\GEOG485\Lesson4\gps_track.txt", "r")
polylineFC = r"C:\PSUGIS\GEOG485\Lesson4\tracklines.shp"
spatialRef = arcpy.Describe(polylineFC).spatialReference
 
# Set up CSV reader and process the header
csvReader = csv.reader(gpsTrack)
header = csvReader.next()
latIndex = header.index("lat")
lonIndex = header.index("long")
 
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
with arcpy.da.InsertCursor(polylineFC, ("SHAPE@",)) as cursor:
    polyline = arcpy.Polyline(vertexArray, spatialRef)
    cursor.insertRow((polyline,))   