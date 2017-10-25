def addPolygon (pointsArray, spatialRef, polygonFC):

    import arcpy
    polygon = arcpy.Polygon(pointsArray, spatialRef)
    with arcpy.da.InsertCursor(polygonFC, ("SHAPE@",)) as cursor:
        cursor.insertRow((polygon,))

    pointsArray.removeAll()



