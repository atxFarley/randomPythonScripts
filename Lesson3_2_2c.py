# Finds the average population in a counties dataset
 
import arcpy
 
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson3\\Pennsylvania\\Counties.shp"
### This row below is new
populationField = "POP1990"
 
rows = arcpy.SearchCursor(featureClass)
row = rows.next()
 
average = 0
totalPopulation = 0
recordsCounted = 0
 
# Loop through each row and keep running total of population
#  and records counted.
 
while row:
### This row below is new
    totalPopulation += row.getValue(populationField)
    recordsCounted += 1
    row = rows.next()
 
average = totalPopulation / recordsCounted
print "Average population for a county is " + str(average) 