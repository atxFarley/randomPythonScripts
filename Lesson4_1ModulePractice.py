import Lesson4_1Practice1

print findPerimeter(4)

fieldsList = listFeatureFields(r"C:\PSUGIS\GEOG485\Lesson3\Project3\CentralAmerica.shp")
for field in fieldsList:
    print field.name

print  findEuclideanDistance(312088, 60271, 312606, 59468)
print findEuclideanDistance(30.346395, -97.720312, 30.338198, -97.718901)