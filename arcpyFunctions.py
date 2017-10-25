def arcmapMessage(messageType, message):
  
    if (messageType == "M"):
        arcpy.AddMessage(message)
    elif (messageType == "E"):
        arcpy.AddError(message)

def arcmapMessage2(messageType, message):

    if (messageType == "M"):
        arcpy.AddMessage(message)
    elif (messageType == "E"):
        arcpy.AddError(message)