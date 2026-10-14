#include<cstdio>
#include<ios>
using namespace std;

int main(){
    
    char M[4][4];
    
    for(int i=0;i<3;i++)scanf("%s",M[i]);
    
    bool ok = true;
    
    if(M[1][2]!=M[1][0])ok = false;
    
    for(int i=0;i<3;i++){
      if(M[0][i]!=M[2][2-i])ok = false;
    }
    
    if(ok)printf("YES\n");
    else printf("NO\n");
  
    
}