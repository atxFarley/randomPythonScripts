import arcpy

#
env.workspace = r"C:\PSUGIS\GEOG485\Lesson2\PracticeExercie5\Lesson2PracticeExercise\Lesson2PracticeExercise\USA.gdb"

iowaPath = r"C:\PSUGIS\GEOG485\Lesson2\PracticeExercie5\Lesson2PracticeExercise\Lesson2PracticeExercise\Iowa.gdb"



fcList = arcpy.ListFeatureClasses()

for featureClass in fcList:
    outName = "Iowa" + featureClass
    arcpy.Clip_analysis(featureClass, iowaPath+r"\Iowa", iowaPath+ "\\" +outName, "")
    print arcpy.GetMessages()


