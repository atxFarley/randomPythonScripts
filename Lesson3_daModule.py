# Finds the average population in a counties dataset
 
import arcpy
 
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson3\\Pennsylvania\\Counties.shp"
populationField = "POP1990"
 
average = 0
totalPopulation = 0
recordsCounted = 0
 
with arcpy.da.SearchCursor(featureClass, (populationField,)) as cursor:
    for row in cursor:
        totalPopulation += row[0]
        recordsCounted += 1
 
average = totalPopulation / recordsCounted
print "Average population for a county is " + str(average)