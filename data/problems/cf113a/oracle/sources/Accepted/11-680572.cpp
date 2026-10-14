#include <iostream>
#include <stdio.h>
#include <string>

using namespace std;

string str[10];
string nm[10000];
string fir;

long long i,j;

int gets(int s)
{
    long long r,t;
for(int i=0;i<6;i++)
{
t=str[i].size();
for(r=nm[s].size();r>-1;r--)
{
if(str[i][t]==nm[s][r])t--;
else break;
if(t==-1)break;
}
if(t==-1)return i;

}
return -1;
}

int main()
{
    str[0]="lios";
    str[1]="liala";
    str[2]="etr";
    str[3]="etra";
    str[4]="initis";
    str[5]="inites";
    getline(cin,fir);
    j=0;
    for(i=0;i<fir.size();i++)
        {if(fir[i]==' '){if(nm[j]!="")j++;continue;}
            nm[j]+=fir[i];
        }
        
    if(j==0 &&gets(0)!=-1)cout<<"YES"<<endl;
    else{
    long long rod=gets(0)%2;
    long long k=1;
    for(i=0;i<=j;i++)
    if(gets(i)!=0+rod)break;
    
    if(gets(i)!=2+rod){k=0;}
    else 
        for(int y=i+1;y<=j;y++)
        if(gets(y)!=4+rod)k=0;
    

    
    
    if(k)cout<<"YES"<<endl;
    else cout<<"NO"<<endl;}

return 0;
}