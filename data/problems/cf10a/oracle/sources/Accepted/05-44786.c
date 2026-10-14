#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

int main()
{

  int n, P1, P2, P3, T1, T2;
  int a[200][2];
  int i,j,k,l;
  int tmp,tmp1,tmp2,tmp3,next,sum;
  scanf("%d%d%d%d%d%d",&n,&P1,&P2,&P3,&T1,&T2);

  for(i=0;i<n;i++)
   scanf("%d%d",&a[i][0],&a[i][1]);

  sum=0;tmp1=0;tmp2=0;tmp3=0;next=0;tmp=0;  
  for(i=0;i<n;i++){
   sum=sum+(a[i][1]-a[i][0])*P1;
   
   if(i+1<n)
       next=a[i+1][0]-a[i][1];
   else 
       next=0;
   
   
   if(next>0){
    
    //printf("%d\n",next);
    if(next>=T1){
      tmp1=T1; tmp+=P1*tmp1;
      next=next-T1;
      }
    else if(next<T1){
      tmp1=next;tmp+=P1*tmp1;
      next=0;goto Down;
      }
     //printf("%d\n",next);
    if(next>=T2){
      tmp2=T2;tmp+=P2*tmp2;
      next=next-T2;
      }
    else if(next<T2){
      tmp2=next;tmp+=P2*tmp2;
      next=0;goto Down;
      }
     //printf("%d\n",next);
    if(next>0){
      tmp3=next;tmp+=P3*tmp3;
      next=0;
      } 
     else{
      next=0;goto Down;
      }
    }
     Down:
     next=0;
     //printf("%d",tmp);
    }

   printf("%d\n",sum+tmp);

return 0;
}