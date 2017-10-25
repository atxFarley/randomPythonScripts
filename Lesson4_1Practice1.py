def findPerimeter(sideLength):
    perimeter = sideLength * 4
    return perimeter



def listFeatureFields(featureClass):
    import arcpy

    fieldsList = arcpy.ListFields(featureClass)
    return fieldsList


def findEuclideanDistance(x1, y1, x2, y2):
    import math
    hypotenuse = (x2-x1)**2 + (y2-y1)**2
    return math.sqrt(hypotenuse)

