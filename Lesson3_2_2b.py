# Finds the average population in a counties dataset
 
import arcpy
 
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson3\\Pennsylvania\\Counties.shp"

#REturns the SEarchCursor object
rows = arcpy.SearchCursor(featureClass)
#Returns the Row object
row = rows.next()
 
average = 0
totalPopulation = 0
recordsCounted = 0
 
# Loop through each row and keep running total of population
#  and records counted.
 
while row:
    totalPopulation += row.POP1990
    recordsCounted += 1
    row = rows.next()
 
average = totalPopulation / recordsCounted
print "Average population for a county is " + str(average)