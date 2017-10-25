# Prints the name of each city in a feature class
 
import arcpy
 
featureClass = "C:\\PSUGIS\\GEOG485\\Lesson3\\USA.gdb\Cities"
 
# Create the search cursor
rows = arcpy.SearchCursor(featureClass)
 
# Call SearchCursor.next() to read the first row
row = rows.next()
 
# Start a loop that will exit when there are no more rows available
while row:
 
    # Do something with the values in the current row     
    print row.NAME
 
    # Call SearchCursor.next() to move on to the next row    
    row = rows.next()