# MXS170018
# 6360.503
# Phase 5
import time
import pickle
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 


def computeDVector(prevD,char, target):
    newD = []
    for num in range(0,len(prevD)):
        if num == 0:
            newD.append(prevD[num]+1)
        else:
            op1 = newD[num-1] + 1 
            op2 = prevD[num] + 1 
            op3 = prevD[num-1] + 1 
            
            parChar = target[num-1]
            if char == 'N':
                op1 -= 1
                op2 -= 1
                op3 -= 1
            elif parChar == 'N':
                op3 = op3-1
            elif parChar == char:
                op3 = op3-1
            
            minima = min(op1,op2,op3)
           
            newD.append(minima)
    
    return newD


def stringMHelper(parE,ChildE,total, rangee):
    occ = []
    if parE == '-':
        for line in total:
            if line[1] == ChildE:
                occ.append(line[0])
    else:
        parOcc = []
        for line in total:
            if line[1] == parE:
                if line[0] >= rangee[0] and line[0] <= rangee[1]:
                    if line[2] == ChildE:
                        occ.append(line[3])
            
    if(len(occ) >= 1):
        return [occ[0],occ[-1]]
    else:
        return []

def stringM(target, total, k,alphabet):
    occurences = []
    Dvectors = {}
    stack = []
    stack.append((0,0,'-',('-',[0,len(total)])))
    #stack.append("-", (1,len(first)))

    
    while(len(stack)>0 ):
        #print(stack)
        depth, depthPar,par, (char,rnge) = stack.pop()
        
        #print(Dvectors)
        
        if (depth <= len(target)+k):
            if(char == '-'):
                dVect = [item for item in range(0,len(target)+1)]
            else:
                dVect = computeDVector(Dvectors[(par,depthPar)],char[-1],target)
            Dvectors[(char,depth)] = dVect

            greaterK = True
            for num in dVect:
                if num <= k:
                    greaterK = False

            if not greaterK:
                if(dVect[len(target)] <= k):
                    
                    occurences.append(char[::-1])
                   
                   #print(occurences)
                else:
                    d2= depth
                    d = depth +1
                    
                    for lettr in reversed(alphabet): #so A is popped first
                        currentChar = char[-1]
                        newRange = stringMHelper(currentChar,lettr,total,rnge)
                        if len(newRange) > 0:
                                childChar = char + lettr
                                stack.append([d,d2,char,(childChar,newRange)])
        
        
    
    return Dvectors,occurences


def reverseString(stri):
    return stri[::-1]

def openAndParse(fileName):
    name = fileName.lower()
    parse = []
    if name == "gorilla":
        
        f = open("gorilla1.dat")
        unparsed = f.readlines()
        f.close()
    
    elif name =="zebrafish":
        
        f = open("zebrafish.dat")
        unparsed = f.readlines()
        f.close()
       
    elif name == "prot1":
        f = open("prot1.txt")
        unparsed = f.readlines()
        f.close()
    elif name =="prot2":
        f = open("prot2.txt")
        unparsed = f.readlines()
        f.close()
    else:
        return "ERRROR"
    
    for lin in unparsed:
        
        a = lin.replace("\n","").replace(" ","")
        b = [i for i in a if i.isalpha()]
        c = "".join(b)
        parse.append(c)

    out = "".join(parse)


    return out

# ONLINE SOLUTION NOT OUR WORK
def approximate_matching_with_k_differences(str1, str2,k):
    # Calculate fuzz ratio (percentage of similarity) between the strings
    fuzz_ratio = fuzz.ratio(str1, str2)
    
    # Calculate partial ratio allowing k differences
    string_differences = (max(len(str1), len(str2)) - (fuzz_ratio * max(len(str1), len(str2))) / 100)
        
    # the score (fuzz raio) is out of 100, so to get the differences in the string we subtract fuzz ratio from 100
    if string_differences <= k:
       # resultant_strings_with_k_diff.append(str1)
        #print(f"The string {str1} and {str2} are approximately similar with differences: {k}")
        return str1
    else:
        #print(f"The string {str1} and {str2} are approximately not similar with differences: {k}")
        return ""
def openBWTPickle(fileName):
    name = fileName.lower()
    bwt = []
    if name == "gorilla":
        print("Gorilla")

        f = open("gorillaBWT",'rb')
        bwt = pickle.load(f)
        f.close()
        

    elif name =="zebrafish":
        
        f = open("zebrafishBWT",'rb')
        bwt = pickle.load(f)
        f.close()
       
    elif name == "prot1":
        print("Prot1")
        f = open("prot1BWT",'rb')
        bwt = pickle.load(f)
        f.close()
    elif name =="prot2":
        print("Prot2")
        f = open("prot2BWT",'rb')
        bwt = pickle.load(f)
        f.close()
    else:
        return "ERRROR"


    return bwt
def testCase1List(targetName, patternDict, KList):
    stats = {}
    for name in targetName:
        total,alphabet = openBWTPickle(name)
        for pattern in patternDict[name]:
            patt = reverseString(pattern)
            for k in KList:
                start = time.time()
                stringM(patt,total,k,alphabet)
                end = time.time()
                index = (name,k,patternDict[name].index(pattern))
                stats[index]=[end-start]
                print(index, stats[index][0])
    

    return stats 
def testCase1Single(targetName, patternList, KList):
    stats = {}
    
        
    total,alphabet = openBWTPickle(targetName)
    for pattern in patternList:
        patt = reverseString(pattern)
        for k in KList:
            start = time.time()
            dVect,occ = stringM(patt,total,k,alphabet)
            
            end = time.time()
            index = (targetName,k,patternList.index(pattern))
            stats[index]=[end-start,occ]
            print(index, stats[index][0])

    return stats 

def partitionPart1(partitionSplit, k, total,alphabet,parsed):
   
    allOcc = []
   
    for subPattern in partitionSplit:
        d,occ = stringM(subPattern, total, k,alphabet)
        allOcc.append(occ)
        checkSpots = []

    counterTemp = 0

    for subPatternOccs in allOcc:
        for occurence in subPatternOccs:
            #print(occurence,occurence[:-1])
            startSpot = parsed.find(occurence[:-1])
            while startSpot > -1:
                checkSpots.append((counterTemp,startSpot+len(occurence)-1))
                #startSpot = parsed.find(occurence[1::][::-1],startSpot+1)
                startSpot = -1
                
        counterTemp = counterTemp + 1
    
    return checkSpots

def partitionPart2(checkSpots,k,charactersPerSub,lengthPattern,pattern,parsed):
    # This currently just for testing if the partition worked. Needs to be changed to instead of the if replace it with a approximate string match algo.
    # Right now it is just testing by seeing if it has found a known occurence of the target.
    tracker = []
    copyList_Partition = []
    flagDupe = True
    for spotToCheck in checkSpots:
        flagDupe = True
        testCopyList_Partition = spotToCheck[1]-(spotToCheck[0]+1)*charactersPerSub+1-k
        for existingTrackers in copyList_Partition:
            if abs(testCopyList_Partition-existingTrackers) < 2*k:
                flagDupe = False
        if flagDupe:
            copyList_Partition.append(testCopyList_Partition)
            tracker.append((parsed[spotToCheck[1]-(spotToCheck[0]+1)*charactersPerSub+1-k:spotToCheck[1]-(spotToCheck[0]+1)*charactersPerSub+1+lengthPattern+k],testCopyList_Partition))
        #resultant_strings_with_k_diff = []
    dupe_grabber_last = []

    for occurence in tracker:
        for i in range(0,2*k):
            similar_string = approximate_matching_with_k_differences(occurence[0][i:len(occurence[0])-(2*k - i)], pattern, k)
            
            if len(similar_string) > 0:
                if occurence[1] not in dupe_grabber_last:
                    dupe_grabber_last.append(occurence[1])

    return dupe_grabber_last


def testCase2List(targetName, patternDict, Klist,l=10):
    stats = {}
    for name in targetName:
        total, alphabet = openBWTPickle(name)
        for pattern in patternDict[name]:
            lengthPattern = len(pattern)
            # Just math.ceil without importing math
            charactersPerSub = -(-lengthPattern//l)
            previousEnd = 0
            
            parsed = openAndParse(name)

            partitionSplit = []
            # Splitting the target string into the smaller sub patterns and reversing each of those
            for num in range(0,l):
                if (num == l-1):
                    partitionSplit.append(pattern[num*charactersPerSub:len(pattern)][::-1])
                else:
                    partitionSplit.append(pattern[num*charactersPerSub:(num+1)*charactersPerSub][::-1])

            for k in Klist:
                smallK = int(k/l)
                startP1 = time.time()
                checkSpots = partitionPart1(partitionSplit,smallK,total,alphabet,parsed)
                endP1 = time.time()
                print(name,"P1",smallK,patternDict[name].index(pattern),endP1-startP1)
                startP2 = time.time()
                # print(checkSpots)
                stuff = partitionPart2(checkSpots,smallK,charactersPerSub,lengthPattern,pattern,parsed)
                endP2 = time.time()
                
                print(name,"P2",k,patternDict[name].index(pattern),endP2-startP2)


def testCase3List(targetName,patternDict,klist,lList):
        for name in targetName:
            total, alphabet = openBWTPickle(name)
            for l in lList:
                for pattern in patternDict[name]:
                    lengthPattern = len(pattern)
                    # Just math.ceil without importing math
                    charactersPerSub = -(-lengthPattern//l)
                    previousEnd = 0
                    
                    parsed = openAndParse(name)

                    partitionSplit = []
                    # Splitting the target string into the smaller sub patterns and reversing each of those
                    for num in range(0,l):
                        if (num == l-1):
                            partitionSplit.append(pattern[num*charactersPerSub:len(pattern)][::-1])
                        else:
                            partitionSplit.append(pattern[num*charactersPerSub:(num+1)*charactersPerSub][::-1])

                    for k in klist:
                        startTime = time.time()
                        smallK = int(k/l)
                        checkSpots = partitionPart1(partitionSplit,smallK,total,alphabet,parsed)
                        stuff = partitionPart2(checkSpots,smallK,charactersPerSub,lengthPattern,pattern,parsed)
                        endTime = time.time()

                        print(name,l, k,patternDict[name].index(pattern),endTime-startTime)


def testCase4List(targetName,patternDict,k=10, l=5):
    stats = {}
    for name in targetName:
        total, alphabet = openBWTPickle(name)
        for pattern in patternDict[name]:
            lengthPattern = len(pattern)
            # Just math.ceil without importing math
            charactersPerSub = -(-lengthPattern//l)
            previousEnd = 0
            
            parsed = openAndParse(name)

            partitionSplit = []
            # Splitting the target string into the smaller sub patterns and reversing each of those
            for num in range(0,l):
                if (num == l-1):
                    partitionSplit.append(pattern[num*charactersPerSub:len(pattern)][::-1])
                else:
                    partitionSplit.append(pattern[num*charactersPerSub:(num+1)*charactersPerSub][::-1])

            
            smallK = int(k/l)
            startTime = time.time()
            checkSpots = partitionPart1(partitionSplit,smallK,total,alphabet,parsed)
                                            
            stuff = partitionPart2(checkSpots,smallK,charactersPerSub,lengthPattern,pattern,parsed)
            endTime = time.time()
            pat = patternDict[name].index(pattern)
            print(name,pat,len(patternDict[name][pat]),endTime-startTime)










dataTry = [ "zebrafish","gorilla","prot1",'prot2'] #
yy= open("tc1Patterns",'rb')
tc1 = pickle.load(yy)
yy.close()

k =  [i for i in range(1,4)]
print(k)
stats = testCase1List(dataTry,tc1,k)

# dataTry = [ "zebrafish","gorilla"] 
# yy= open("tc23Patterns",'rb')
# tc23 = pickle.load(yy)
# yy.close()

# k =  [10,20,30]
# print(k)
# testCase2List(dataTry,tc23,k,10)


# print(k)
# lList = [10,12,15]
# print(lList)
# testCase3List(dataTry,tc23,k,lList)


# dataTry = [ "zebrafish","gorilla","prot1",'prot2'] 
# yy= open("tc4Patterns",'rb')
# tc4 = pickle.load(yy)
# yy.close()
# testCase4List(dataTry,tc4,k=10,l=5)
