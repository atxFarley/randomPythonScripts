from jpype import *
print "Start JVM"
try:
    startJVM(r"C:\Java\32bit\jdk1.7_80\jre\bin\server\jvm.dll", "-Xms64m", "-Xmx256m", "-ea", "-Djava.class.path=C:\\PSUGIS\\GEOG485\\scripts\\classes")
    #print "JVM started"
    java.lang.System.out.println("hello world")

    #z = java.rmi.Naming.lookup("rmi://bzip4.flooddata.com:12346/zip4");

    #print z, z.__class__

    #z4Model = z.addressInquiry("1206 Morrow Avenue", "austin", "texas", "78757");
    #java.lang.System.out.println("\tInput Address: " + z4Model.iadl1 + " (street), " + z4Model.ictyi + " (city), " + z4Model.istai + " (state), " + z4Model.izipc + " (zipcode)");
    #java.lang.System.out.println("\tOutput Address: " + z4Model.dadl1 + " (street), " + z4Model.dctya + " (city), " + z4Model.dstaa + " (state), " + z4Model.zipc + " (zipcode), " + z4Model.addon + " (addon), " + z4Model.ppnum + " (ppnum), " + z4Model.str_name + " (streetname), " + z4Model.psnum + " (psnum), " + z4Model.punit+ " (punit), " + z4Model.rec_type + " (rec_type), " + z4Model.county + " (countcode)");
    #java.lang.System.out.println("\tParsed Address: " + z4Model.pre_dir + " (pre_dir), " + z4Model.str_name + " (streetname), " + z4Model.suffix + " (suffix), " + z4Model.post_dir + " (post_dir)");
    #java.lang.System.out.println("\tParsed Address2: " + z4Model.ppnum + " (ppnum) " + z4Model.ppre1 + " (ppre1), " + z4Model.ppre2 + " (ppre2), " + z4Model.ppnam + " (ppnam), " + z4Model.psuf2 + " (psuf2), " + z4Model.ppst1 + " (ppst1), " + z4Model.ppst2 + " (ppst2)");

    shutdownJVM()
except Exception as e:
    print "Exception caught {0}".format(e.args[0])