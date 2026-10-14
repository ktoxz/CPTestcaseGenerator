#include <cstdio>
#include <iostream>
using namespace std;

bool palind(int a,int b){
    string sa,sb;
    if (a<10){
        sa+='0';
        sa+=(a+'0');
    }
    else{
        sa+=((a/10)+'0');
        sa+=((a%10)+'0');
    }
    if (b<10){
        sb+='0';
        sb+=(b+'0');
    }
    else{
        sb+=((b/10)+'0');
        sb+=((b%10)+'0');
    }
    if (sa[0]==sb[1] && sa[1]==sb[0])
        return 1;
    return 0;
}

void cetak (int a,int b){
    string sa,sb;
    if (a<10){
        sa+='0';
        sa+=(a+'0');
    }
    else{
        sa+=((a/10)+'0');
        sa+=((a%10)+'0');
    }
    if (b<10){
        sb+='0';
        sb+=(b+'0');
    }
    else{
        sb+=((b/10)+'0');
        sb+=((b%10)+'0');
    }
    cout << sa << ":" << sb << endl;
}

int main(){
    string str;
    int a,b;
    char c;
    bool cb=1;
    cin >> a >> c >> b;
    for (int i=a;;i=(i+1)%24){
        if (cb){
            cb=0;
            for (int j=b+1;j<60;++j){
                if (palind(i,j)){
                    cetak(i,j);
                    return 0;
                }
            }
        }
        else{
            for (int j=0;j<60;++j){
                if (palind(i,j)){
                    cetak(i,j);
                    return 0;
                }
            }
        }
    }
    return 0;
}