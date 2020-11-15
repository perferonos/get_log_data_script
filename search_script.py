import re, sys
import os.path
from operator import itemgetter

BAR = '-------------------------------------------------------'
LINE0 = '|  Name  | Stat 0 | Stat 1 | Stat 2 | Stat 3 | Stat 4 |'

# asks for path
def askForPath():
    print("Please, enter the path:")
    path = input()
    return path

# get path as argument
def getPath():
    if len(sys.argv) < 2: # if there is no second argument in console
        path = askForPath()
    else:
        path = sys.argv[1]
    return path

# returns a list of names of directories from path
def getDirsNames(path):
    dirs = os.listdir(path)
    for direc in dirs: # we need only directories
        if '.' in direc:
            dirs.remove(direc)
    return dirs

# transforming a string with stat numbers to list
def _getListOfNums(statStr):
    numList = [int(x) for x in statStr.split()]
    return numList

# summing the numbers of statistics and returning a list of summs
def statSum(statList, testName):
    result = [0, 0, 0, 0, 0, 0]
    for unit in statList:
        unit = _getListOfNums(unit)
        for i in range(1, len(result)):
            result[i] += unit[i-1]
    result[0] = testName
    return result

# searches for statiscics in files and returnes a list of lines with ones
def statSearch(path):
    stats = []
    fd = open(path, 'r')
    for line in fd:
        if "Statistics:" in line:
            st = re.sub(r"\d\d:\d\d:\d\d.\d\d\d\d\d\d] Statistics: ", "", line) # cleaning left side
            st = re.sub(r"\n", "", st) # cleaning right side
            stats.append(st)
    return stats


# building result lines
def buildResLine(line):
    resLine = ""
    for unit in line:
        unit = str(unit)
        resLine += "| " + unit + " "*(7 - len(unit))
    resLine += "|"
    return resLine


if __name__ == "__main__":
    print(BAR)
    path = getPath()
    print(BAR)
    dirs = getDirsNames(path) # getting names of directories
    line = []
    statistics = []
    for direc in dirs:
        lfname = path + direc + '/' + direc + '.log' # log file name
        statVals = statSearch(lfname)
        statistics.append(statSum(statVals, direc))
    statistics = sorted(statistics, key=itemgetter(1), reverse=True) # sorting by descent order
    
    print(BAR)
    print(LINE0)
    print(BAR)
    for line in statistics: # result output
        print(buildResLine(line)) 
        print(BAR)
        
