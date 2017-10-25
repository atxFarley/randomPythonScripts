import arcpy

arcpy.env.overwriteOutput = True
parkAndRides = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseC\Washington.gdb\ParkAndRide"
arcpy.env.workspace = r"C:\PSUGIS\GEOG485\Lesson3\Lesson3PracticeExercises\Lesson3PracticeExercises\Lesson3PracticeExerciseC\Washington.gdb"
capacityField = "Approx_Par"

whereClause = '"'+str(capacityField) + '" >  500'  


arcpy.MakeFeatureLayer_management(parkAndRides,"PandRLayer", whereClause)

arcpy.CopyFeatures_management("PandRLayer", "largeCapacityParkAndRide")






arcpy.Delete_management("PandRLayer")


print "Total Cities {0}".format(intTotalCities)
print "Total Cities with at least two Park & Ride Services {0}".format(intCitiesWithPandR)

print "Percentage of cities with at least two park & ride services is {0}%".format((float(intCitiesWithPandR)/float(intTotalCities))*100)






