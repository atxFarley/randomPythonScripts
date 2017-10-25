import csv

gpsTrack = open(r"C:\PSUGIS\GEOG485\Lesson4\gps_track.txt", "r")

csvReader = csv.reader(gpsTrack)

header = csvReader.next()

latIndex = header.index("lat")
lonIndex = header.index("long")

# Make an empty list
coordList = []

# Loop through the lines in the file and get each coordinate
for row in csvReader:
    lat = row[latIndex]
    lon = row[lonIndex]
    coordList.append([lat,lon])

# Print the coordinate list
print coordList