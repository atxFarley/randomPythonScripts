import random
 
# Choose a random school from a list and print it
schools = ["Penn State", "Michigan", "Ohio State", "Indiana"]
randomSchoolIndex = random.randrange(0,4)
chosenSchool = schools[randomSchoolIndex]
print chosenSchool
 
# Depending on the school, print the mascot
if chosenSchool == "Penn State":
    print "You're a Nittany Lion"
elif chosenSchool == "Michigan":
    print "You're a Wolverine"
elif chosenSchool == "Ohio State":
    print "You're a Buckeye"
elif chosenSchool == "Indiana":
    print "You're a Hoosier"
else:
    print "This program has an error"