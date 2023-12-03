
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
            
            if target[num-1] == char:
                op3 = op3-1
            
            # if(char == 'a'):
            #     print("\n",op1,op2,op3)
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
    
    
    
    while(len(stack)>0):
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




def approximate_matching_with_k_differences(str1, str2, k):
    # Calculate fuzz ratio (percentage of similarity) between the strings
    fuzz_ratio = fuzz.ratio(str1, str2)
    
    # Calculate partial ratio allowing k differences
    string_differences = (max(len(str1), len(str2)) - (fuzz_ratio * max(len(str1), len(str2))) / 100)
        
    # the score (fuzz raio) is out of 100, so to get the differences in the string we subtract fuzz ratio from 100
    if string_differences <= k:
        #resultant_strings_with_k_diff.append(str1)
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
        print("Zebra")
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

def testCase2():
    print("WOW")

dataTry = ["zebrafish","gorilla", "prot1",'prot2'] #

yy= open("tc1Patterns",'rb')
tc1 = pickle.load(yy)
yy.close()



k =  [i for i in range(1,5)]
print(k)

nini = time.time()
stats = testCase1List(dataTry,tc1,k)
mimi = time.time()

print(mimi-nini)




