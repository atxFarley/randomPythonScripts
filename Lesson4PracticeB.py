def addTeamGoals(map, team, goals):
    print team + ": " + goals
    if (team in map.keys()):
        print team + " in map already"
        currentTally = map[team]
        map[team] = int(currentTally) + int(goals)
    else:
        print "adding " + team + " to map"
        map[team] = int(goals)
    

import csv

scoresFile = open(r"C:\PSUGIS\GEOG485\Lesson4\Lesson4PracticeExercises\Lesson4PracticeExerciseB\Scores.txt", "rU")

csvReader = csv.reader(scoresFile, delimiter=" ")

header = csvReader.next()
winner = header.index("Winner")
wingoals = header.index("WG")
loser = header.index("Loser")
losegoals = header.index("LG")
print "indexes  winner {0}, winner goals {1}, loser {2}, loser goals {3}".format(str(winner), str(wingoals), str(loser), str(losegoals)) 

teamGoalsMap = {}

for row in csvReader:
    addTeamGoals(teamGoalsMap, row[winner], row[wingoals])
    addTeamGoals(teamGoalsMap, row[loser], row[losegoals])

print teamGoalsMap
        
                     