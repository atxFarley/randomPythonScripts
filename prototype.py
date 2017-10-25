import jpypeModule
import arcpyFunctions

try:
    #myList = [1, 2, "cookie jar", [64, "crumbs"], 51094]
    #print myList
    #colorList = ["Red", "Green", ["Navy", "Cornflower", "Teal"], "Yellow"]
    #print colorList[3]
    #varTestQuotes = "Amy is 'Awesome'"
    #print varTestQuotes
    #varTestQuotes2 = 'Amy is "Awesome"'
    #print varTestQuotes2
    jpypeModule.validateJVMPath()
    jpypeModule.validateZip4Classpath()
    jpypeModule.launchJVM()
    arcpyFunctions.arcmapMessage("M", "calling USPS")
    for x in range(10):
        #jpypeModule.uspszip4()
        arcpyFunctions.arcmapMessage("M", "USPS called for {0}".format(str(x)))
    #jpypeModule.shutdownJava()
    arcpyFunctions.arcmapMessage("M", "JVM shutdown complete")
except Exception as e:
    print "Exception caught in prototype {0}".format(e.args[0])
    arcpyFunctions.arcmapMessage2("E", "calling USPS")