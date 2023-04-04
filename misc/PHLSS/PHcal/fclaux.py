import numpy as np
import param as par


def loadfile(fname):
    '''only works for well-formed text file of space-separated doubles'''

    rows = []  # Unknown number of lines, so use list
    with open(fname) as f:
        for line in f:
            line = [float(s) for s in line.split()[:4]]  # Select only Mass and Pos(3) by [:4], i.e. 0, 1, 2, 3
            rows.append(np.array(line, dtype=np.double))
    
    return rows  # Convert list of vectors to array


def savePD(d, filename, savePrefix):  # d is the "list of pairs(dimension, pair(birth, death)) – the persistence of the complex"
    toSave = []
    if par.method == 0:
        for elm in d:
            if elm[1][1] != elm[1][0]:  # If birth != death
                toSave.append([elm[0], np.sqrt(elm[1][0]), np.sqrt(elm[1][1])])   
    else:
        for elm in d:
            if elm[1][1] != elm[1][0]:  # If birth != death
                toSave.append([elm[0], elm[1][0], elm[1][1]])
    
    # f = open(savePrefix+".txt", "a")
    # toSave = np.reshape(toSave, (1, -1))
    # np.savetxt(f, toSave, newline=" ")
    # f.write("\n")
    # f.close()

    np.save(savePrefix, np.array(toSave).astype("float32"))


def cleanPD(pd, cut, power=0.5):  # Apply cuts onto PDs?
    p0 = []
    p1 = []
    p2 = []
    for elm in pd:
        if elm[0] == 2 and elm[1][1] != elm[1][0] and elm[1][1] > (float(cut) / 2)**2:  # If it is a 2-cycle, birth != death and death > cut (= 0)
            p2.append([np.power(elm[1][0], power), np.power(elm[1][1] - elm[1][0], power)])  # [birth, persistence]
        
        elif elm[0] == 1 and elm[1][1] != elm[1][0] and elm[1][1] > (float(cut) / 2)**2:
            p1.append([np.power(elm[1][0], power), np.power(elm[1][1] - elm[1][0], power)])
        
        elif (np.isinf(elm[1][1])) == False and elm[1][1] != elm[1][0] and elm[1][1] > (float(cut) / 2)**2:  # If death is not infinite, birth != death and death > cut (= 0) 
            p0.append([np.power(elm[1][0], power), np.power(elm[1][1] - elm[1][0], power)])
    return np.array(p0), np.array(p1), np.array(p2)
