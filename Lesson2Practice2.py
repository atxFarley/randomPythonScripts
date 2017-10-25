beatles = ["John Lennon", "Paul McCartney", "Ringo Starr", "George Harrison"]

for name in beatles:
    spaceIndex = name.index(" ")
    print "There is a space in " + name + "'s name at character " + str(spaceIndex)
    first = name[:spaceIndex]
    print first
    last = name[spaceIndex+1:]
    print last
    print last + ", " + first