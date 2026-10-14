#include <cmath>

#include <queue>

#include <cstdio>

#include <map>

#include <vector>

#include <iostream>

#include <stack>

#include <climits>

#include <queue>

#include <algorithm>

using namespace std;



int main(int argc, const char * argv[]) {



    string a,b;

    cin>>a>>b;

    if(b.length() != a.length()){

        cout<<"WRONG_ANSWER"<<endl;

        return 0;

    }

    

    bool num = false;

    bool zero = false;

    for(int i = 0; i < b.length(); i++){

        if(b[i] != '0'){

            num = true;

        }

        if(num == false && b[i] == '0'){

            zero = true;

        }

    }

    if(num == true && zero == true){

        cout<<"WRONG_ANSWER"<<endl;

        return 0;



    }

    

    int arrn[10] = {0};

    int arrm[10] = {0};

    

    

    

    for(int i = 0; i < a.length(); i++){

        if(i+1 < a.length() && b[i] > b[i+1] && b[i+1] != '0'){

            cout<<"WRONG_ANSWER"<<endl;

            return 0;

        }

        

        char c = b[i];

        char d = a[i];

        arrm[c-'0']++;

        arrn[d-'0']++;

    }

    

    for(int i = 0; i < 10; i++){

        if(arrm[i] != arrn[i]){

            cout<<"WRONG_ANSWER"<<endl;

            return 0;

        }

    }

    

    for(int i = 1; i <= arrm[0] && i < b.size(); i++){

        if(b[i] != '0'){

            cout<<"WRONG_ANSWER"<<endl;

            return 0;

        }

    }

    

    cout<<"OK"<<endl;

    

    return 0;

}