import random


spinnerChoices = [-1, -2, -3, -4, 2, 2, 10]
intTurnsToWin = 0   
turn = 1
try: 
    while turn < 10001:
        #print turn
        intTurnsAtStart = 0
        intCherriesStart = 10
        
        
        while intCherriesStart > 0:
            #Spin the spinner
            spinIndex = random.randrange(0,7)
            spinResult = spinnerChoices[spinIndex]

            #print "You spun a " + str(spinResult) + "."

            intCherriesStart +=spinResult

            if intCherriesStart > 10:
                intCherriesStart = 10
            elif intCherriesStart < 0:
                intCherriesStart = 0

            #print "You have " + str(intCherriesStart) + " on your tree."

            intTurnsAtStart += 1

        #print "It took you " + str(intTurnsAtStart) + " turns to win the game."
        intTurnsToWin += intTurnsAtStart
        print "Total after game: "  + str(turn) +  ", Turns: " + str(intTurnsAtStart) +  " Running Total: " + str( intTurnsToWin)
        turn += 1
         

    intAvg = intTurnsToWin / 10000
    print "Turns to Win Total: " + str(intTurnsToWin)
    print "Average: " + str(intAvg)
except Exception as e:
    print e
#lastline = raw_input(">")
