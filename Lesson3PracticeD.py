import arcpy

arcpy.env.overwriteOutput = True
cityBoundaries = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseD\Washington.gdb\CityBoundaries"
parkAndRides = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseD\Washington.gdb\ParkAndRide"
arcpy.env.workspace = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseD\Washington.gdb"
cityIDStringField = "CI_FIPS"             # Name of column with city IDs
cityNameField = "NAME"

intTotalCities = 0
#Get Total Cities Count
citiesResult = arcpy.GetCount_management(cityBoundaries)
intTotalCities = int(citiesResult.getOutput(0))
print "Total Cities {0}".format(intTotalCities )

arcpy.MakeFeatureLayer_management(parkAndRides,"PandRLayer")

with arcpy.da.UpdateCursor (cityBoundaries, (cityIDStringField,cityNameField)) as cursor:
    for row in cursor:
        print str(row[0]) + "  - " + str(row[1])
        whereClause = '"' + str(cityIDStringField) + '" = '+"'"+str(row[0]) + "'"
        arcpy.MakeFeatureLayer_management(cityBoundaries, "CityLayer", whereClause)
        arcpy.SelectLayerByLocation_management("PandRLayer","COMPLETELY_WITHIN","CityLayer")
        outputFeatureClassName = str(row[1]).replace(" ", "")+ "_parkAndRides"
        print outputFeatureClassName
        arcpy.CopyFeatures_management("PandRLayer", outputFeatureClassName)

        arcpy.Delete_management("CityLayer")



arcpy.Delete_management("PandRLayer")