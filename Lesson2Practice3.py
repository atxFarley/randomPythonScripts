score = input()
letterGrade = ""
try:
    score = int(score)
    
    if (score < 60):
        letterGrade = "F"
    elif (score >=60 and score < 70):
        letterGrade="D"
    elif (score >=70 and score < 80):
        letterGrade="C"
    elif (score >=80 and score < 90):
        letterGrade="B"
    elif (score >=90 and score < 100):
        letterGrade="A"
    else:
        print "Invalid Score"

    print "Letter Grade: " + letterGrade
except:
    print "Invalid Score.  Please Enter an integer value."