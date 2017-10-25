import arcpy

arcpy.env.overwriteOutput = True
cityBoundaries = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseB\Washington.gdb\CityBoundaries"
parkAndRides = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseB\Washington.gdb\ParkAndRide"

cityNameField = "NAME"
cityHasParkRideField = "HasTwoParkAndRides"

intTotalCities = 0
#Get Total Cities Count
citiesResult = arcpy.GetCount_management(cityBoundaries)
intTotalCities = int(citiesResult.getOutput(0))
print "Total Cities {0}".format(intTotalCities )

intCitiesWithPandR = 0

#Make temporary feature layers

arcpy.MakeFeatureLayer_management(parkAndRides,"PandRLayer")

#obtain Update Cursor to iterate through the cities feature class
with arcpy.da.UpdateCursor (cityBoundaries, (cityHasParkRideField, "NAME")) as cursor:
    for row in cursor:
        print row[1]
        whereClause = '"NAME"='+"'"+str(row[1]) + "'"
        arcpy.MakeFeatureLayer_management(cityBoundaries, "CityLayer", whereClause)
        arcpy.SelectLayerByLocation_management("PandRLayer","COMPLETELY_WITHIN","CityLayer")
        prResult = arcpy.GetCount_management("PandRLayer")
        intPandR = int(prResult.getOutput(0))
        if (intPandR >= 2):
            row[0] = "True"
            cursor.updateRow(row)
            intCitiesWithPandR += 1

        arcpy.Delete_management("CityLayer")



arcpy.Delete_management("PandRLayer")


print "Total Cities {0}".format(intTotalCities)
print "Total Cities with at least two Park & Ride Services {0}".format(intCitiesWithPandR)

print "Percentage of cities with at least two park & ride services is {0}%".format((float(intCitiesWithPandR)/float(intTotalCities))*100)






