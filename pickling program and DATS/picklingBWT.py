import pickle 
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
#yy = open('prot1BWT','wb')


stri = "prot1"
#stri = "gorilla"
#stri = "prot1"
#stri = "prot2"

g = openAndParse(stri)
print(stri,len(g))

start = time.time()
bwt = totalBWT(g)
end = time.time()

print(end-start)

yy = open(stri+"BWT",'wb')

pickle.dump(bwt,yy)
yy.close()

xx = open(stri+"BWT",'rb')
check = pickle.load(xx)
xx.close()

if check == bwt:
    print("SUCESS")
