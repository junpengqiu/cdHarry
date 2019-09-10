import sys
import random
def getLinesFromFile(fname):
    with open(fname) as f:
        toRet = []
        for l in f.readlines():
            toRet.append(l.strip())
        return toRet

def endWith(testStr, endStr):
    return len(testStr) >= len(endStr) and testStr[(len(testStr) - len(endStr)):len(testStr)] == endStr

def getLineHead(line):
    lineSplit = line.split(":")
    if len(lineSplit) <= 1:
        return ""

    return lineSplit[0]

def parseLine(line):
    lineHead = getLineHead(line)

    if (lineHead == "") or ("ENCODING" in line):
    	return "UPDATE_VAL"

    if lineHead == "END":
        return "SAVE_AND_NEW"

    endStrNotGoToKey = {"UID", "CATEGORIES", "REV"}
    for str in endStrNotGoToKey:
        if endWith(lineHead, str):
            return "UPDATE_VAL"
    
    return "UPADATE_BOTH"

def getUniqueCards(lines):
    distLinesToWholeLines = dict()
    keyCur = ""
    valCur = ""
    # print("number of lines to be processed: " + str(len(lines)))
    cnt = 0
    for line in lines:
        # print("lenght of line is " + str(len(line)))
        # if cnt % 50 == 0:
            # print(str(cnt) + " lines processed")
        parseResult = parseLine(line)
        cnt += 1

        if parseResult == "UPADATE_BOTH":
            keyCur += line + "\n"
            valCur += line + "\n"
            continue

        if parseResult == "UPDATE_VAL":
            valCur += line + "\n"
            continue

        if parseResult == "SAVE_AND_NEW":
            keyCur += line + "\n"
            valCur += line + "\n"
            if (keyCur not in distLinesToWholeLines) or (len(valCur) < len(distLinesToWholeLines[keyCur])):
                distLinesToWholeLines[keyCur] = valCur

            keyCur = ""
            valCur = ""
            continue

        if parseResult == "SKIP":
            continue

        sys.exit("case \"" + parseResult + "\" NOT KNOWN")

    return [v for (_, v) in distLinesToWholeLines.items()]
    # return [k for (k, _) in distLinesToWholeLines.items()]

def writeToNewFile(toWrite):
    randNum = random.randrange(99999)
    fname = ((sys.argv[1]).split(".")[0]) + str(randNum) + ".vcf"
    with open(fname, "w+") as f:
        for l in toWrite:
            f.write(l)
    print("new file (" + fname + ") has been created with the deduped contacts")

def main():
    lines = getLinesFromFile(sys.argv[1])

    numOrig = sum([ifEnd for ifEnd in map(lambda l: getLineHead(l) == "END", lines)])
    print(str(numOrig) + " contacts before dedupe")

    toWrite = getUniqueCards(lines)
    print(str(len(toWrite)) + " contacts after dedupe")
    # print("\n=========\n")
    # for l in toWrite:
    #     print("one:")
    #     print(l)
    # print("\n=========\n")
    writeToNewFile(toWrite)
    
if __name__ == "__main__":
    main()