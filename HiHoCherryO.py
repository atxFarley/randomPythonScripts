import random


intCherriesStart = 10
intTurnsAtStart = 0

spinnerChoices = [-1, -2, -3, -4, 2, 2, 10]


while intCherriesStart > 0:
    #Spin the spinner
    spinIndex = random.randrange(0,7)
    spinResult = spinnerChoices[spinIndex]

    print "You spun a " + str(spinResult) + "."

    intCherriesStart +=spinResult

    if intCherriesStart > 10:
        intCherriesStart = 10
    elif intCherriesStart < 0:
        intCherriesStart = 0

    print "You have " + str(intCherriesStart) + " on your tree."

    intTurnsAtStart += 1

print "It took you " + str(intTurnsAtStart) + " turns to win the game."
lastline = raw_input(">")
