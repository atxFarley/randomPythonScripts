    # This script uses map algebra to find values in an
#  elevation raster greater than 3500 (meters).
 
import arcpy
from arcpy.sa import *

arcpy.env.overwriteOutput = True
 
# Specify the input raster
inRaster = "C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\foxlake"
cutoffElevation = 5500
 
# Check out the Spatial Analyst extension
arcpy.CheckOutExtension("Spatial")
 
# Make a map algebra expression and save the resulting raster
outRaster = Raster(inRaster) > cutoffElevation
outRaster.save("C:\\PSUGIS\\GEOG485\\Lesson1\\Lesson1\\foxlake_hi_10")
     
# Check in the Spatial Analyst extension now that you're done
arcpy.CheckInExtension("Spatial")