import arcpy

arcpy.env.overwriteOutput = True
cityBoundaries = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseA\Washington.gdb\CityBoundaries"
parkAndRides = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseA\Washington.gdb\ParkAndRide"

cityNameField = "NAME"
cityHasParkRideField = "HasParkAndRide"

intTotalCities = 0
#Get Total Cities Count
citiesResult = arcpy.GetCount_management(cityBoundaries)
intTotalCities = int(citiesResult.getOutput(0))
print "Total Cities {0}".format(intTotalCities )

intCitiesWithPandR = 0

#Make temporary feature layers
 
arcpy.MakeFeatureLayer_management(cityBoundaries, "CitiesLayer")
 

arcpy.MakeFeatureLayer_management(parkAndRides,"PandRLayer")


#Do Select by Location to get a temp layer of cities with park & ride
# Apply a selection to the US States layer
arcpy.SelectLayerByLocation_management("CitiesLayer","CONTAINS","PandRLayer")
 

#obtain Update Cursor to iterate through the temp layer and update the HasParkAndRide field of the
#parkAndRides feature class
with arcpy.da.UpdateCursor ("CitiesLayer", (cityHasParkRideField, "NAME")) as cursor:
    for row in cursor:
        print row[1]
        row[0] = "True"
        cursor.updateRow(row)
        intCitiesWithPandR += 1


print "Total Cities {0}".format(intTotalCities)
print "Total Cities with Park & Ride Services {0}".format(intCitiesWithPandR)

print "Percentage of cities with park & ride services is {0}%".format((float(intCitiesWithPandR)/float(intTotalCities))*100)






