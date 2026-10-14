#include <stdio.h>
#include <string.h>
#include <iostream>
#include <map>
#include <algorithm>

using namespace std;


char word[100003];
int n,k;

int alph[26];

char findmin() {
    int mn=0;
    char ret=0;
    for (int i=0;i<26;++i) {
//      printf("%d) %d\n", i, alph[i]);
        if ((mn==0||alph[i]<mn)&&alph[i]>0) {
            mn=alph[i];
            ret=(char)(i+'a');
        }
    }
    
//  printf("ret=%c\n", ret);
    return ret;
}

int main() {
    
    cin>>word>>k;
    
    n=strlen(word);
    
    for (int i=0;i<n;++i) {
        alph[word[i]-'a']++;
    }
    
    char c;
    int f;
    
    while (k) {
        c=findmin();
        if (!c) break;
        f=alph[c-'a'];
//      printf("found %c f=%d n=%d\n", c, f, n);
        if (f>k) break;
    
        k-=f;
        alph[c-'a']=-1;
    }
    
    int cnt=0;
    for (int i=0;i<26;++i) if (alph[i]>0) ++cnt;
    
    cout<<cnt<<endl;
    
    for (int i=0;i<n;++i) {
        c=word[i];
        if (alph[c-'a']>0) cout<<c;
    }
    cout<<endl;
    return 0;
}