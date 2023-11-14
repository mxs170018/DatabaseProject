#include <iostream>

#include <divsufsort.h>
#include <fstream>
#include <string>
#include <istream>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
using namespace std;


// STACK OVERFLOW
bool is_number(const std::string& s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isdigit(*it)) ++it;
    return !s.empty() && it == s.end();
}

// GEEKS FOR GEEKS
string tokenize(string s, string del = " ")
{
    string muhReturn = "";
    int start, end = -1*del.size();
    do {
        start = end + del.size();
        end = s.find(del, start);

        string potential = s.substr(start, end - start);
        if(is_number(potential)){

        }else{
            muhReturn += potential;
        }
        
    } while (end != -1);

    return muhReturn;
}
int main(){

    //string wawa = "4201 TTCTTATTCG TGGCTTTGGT TATTTGTCTC GTTCTTCGGT CCTTCTTGAT CAGTCTTGAN";
    //string baba = tokenize(wawa," ");
    //cout << baba << endl;
    string lol = "MAMA";
    string lol2 = "EATS";
    cout << lol+lol2 << endl;


    string dna = "";
    string myText; 
    ifstream MyReadFile("testing.txt");
    bool origin = false;
    while(getline(MyReadFile,myText)){
        if(origin == false){
            if(myText == "ORIGIN"){
                origin = true;
            }
        }else{
            dna += tokenize(myText," ");
        }
        
    }

    MyReadFile.close();

    //cout << dna << endl;


    // DIVSUFSORT EXAMPLE THAT DOESNT WORK
    const char* charDNA = dna.c_str();
    
    int n = strlen(charDNA);

    int i, j;

    int *SA = (int *)malloc(n * sizeof(int));

    divsufsort((unsigned char *)charDNA, SA, n);

    for(i = 0; i < n; ++i) {
        printf("SA[%2d] = %2d: ", i, SA[i]);
        for(j = SA[i]; j < n; ++j) {
            printf("%c", charDNA[j]);
        }
        printf("$\n");
    }

    // deallocate
    free(SA);

}