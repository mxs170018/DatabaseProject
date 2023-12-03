
import time
# GEEKS FOR GEEKS
# This code is contributed by Susobhan Akhuli

def compute_suffix_array(input_text, len_text):

    # Array of structures to store rotations and their indexes
    suff = [(i, input_text[i:]) for i in range(len_text)]

    # Sorts rotations using comparison function defined above
    suff.sort(key=lambda x: x[1])
    
    first = ""
    for seg in suff:
        first += seg[1][0]

    # Stores the indexes of sorted rotations
    suffix_arr = [i for i, _ in suff]
 

    # Returns the computed suffix array
    return suffix_arr,first 
 
# Takes suffix array and its size as arguments
# and returns the Burrows-Wheeler Transform of given text

def find_last_char(input_text, suffix_arr, n):

    # Iterates over the suffix array to
    # find the last char of each cyclic rotation
    bwt_arr = ""

    for i in range(n):
        # Computes the last char which is given by 
        # input_text[(suffix_arr[i] + n - 1) % n]
        j = suffix_arr[i] - 1

        if j < 0:
            j = j + n

        bwt_arr += input_text[j]
 
    # Returns the computed Burrows-Wheeler Transform
    return bwt_arr
 


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

def getAlphabet(str2):
    return sorted(list(set(str2)))


def getAlphabetNoDollar(str2):
    str3 = str2.replace('$','')
    return sorted(list(set(str3)))
    #return list(set(str3))
    
def getFrequency(str):
    alpha = getAlphabet(str)
    freqC = [0 for _ in range(0,len(alpha))]
    freq = []
    for ch in str:
        freqC[alpha.index(ch)] += 1
        curr = freqC[alpha.index(ch)]
        if ch == '$':
            freq.append(0)
        else: 
            freq.append(curr)
    
    return freq


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


def openAndParse(fileName):
    name = fileName.lower()
    parse = []
    if name == "gorilla":
        print("Gorrilla")

        f = open("gorilla1.dat")
        unparsed = f.readlines()
        f.close()
        

    elif name =="zebrafish":
        print("Zebra")
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
    
    print(len(unparsed),len(unparsed[0]))
    for lin in unparsed:
        
        a = lin.replace("\n","").replace(" ","")

        b = [i for i in a if i.isalpha()]
        c = "".join(b)
        parse.append(c)

    out = "".join(parse)


    return out+"$"



def totalBWT(parsed):
    sa,first = compute_suffix_array(parsed,len(parsed))
    sa,first = compute_suffix_array(parsed,len(parsed))
    bwt = find_last_char(parsed,sa,len(parsed))

    alphabet = getAlphabetNoDollar(first)
    freqF = getFrequency(first)
    freqL = getFrequency(bwt)

    total = []
    for i in range(0,len(first)):
        total.append([freqF[i],first[i],bwt[i],freqL[i]])
    print("Alpha",alphabet)
    return total,alphabet

def testCase1Dict(targetName, patternDict, KList):
    stats = {}
    for name in targetName:
        parse = openAndParse(name)
        total = totalBWT(parse)
        for pattern in patternDict[name]:
            patt = reverseString(pattern)
            for k in KList:
                start = time.time()
                _,occ = stringM(patt,total,k)
                end = time.time()
                
                stats[(name,k)]=[end-start,occ]

    return stats 
def testCase1List(targetName, patternList, KList):
    stats = {}
    for name in targetName:
        parse = openAndParse(name)
        total,alphabet = totalBWT(parse)
        for pattern in patternList:
            patt = reverseString(pattern)
            for k in KList:
                start = time.time()
                dVect,occ = stringM(patt,total,k,alphabet)
                print("AHH",occ)
                end = time.time()
                stats[(name,k,patternList.index(pattern))]=[end-start,occ]

    return stats 

def testCase2():
    print("WOW")

patternList = ["NMMFGKIQHWYRLSSV","LRPYTTLTTIAIIWMCPHIYSGHIPDQP"]
k =  [i for i in range(1,4)]
print(k)
stats = testCase1List(["prot2"],patternList,k)

print(stats)


