#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#define MAX 1010
int main()
{
   int n,p,i,ans;
   int min[MAX],goesto[MAX],comesfrom[MAX],dia[MAX],thetank[MAX],thetap[MAX];
   int tank,tap,from,to,qty;
   memset(goesto,0,sizeof(goesto));
   memset(comesfrom,0,sizeof(comesfrom));


   scanf("%d%d",&n,&p);
   for(;p;p--){
      scanf("%d%d%d",&from,&to,&qty);
      goesto[from]=to;
      comesfrom[to]=from;
      dia[from]=qty;
   }
   ans=1;

   for(i=1;i<=n;i++)
      if(goesto[i] && (comesfrom[i]==0)){//i is a tank
  //       printf("%d is a tank\n",i);
         thetank[ans]=tank=i;
         min[ans]=dia[tank];

         while(tank=goesto[tank]){
//         printf("the diameter so far is %d\n",min[ans]);
            if(goesto[tank] && min[ans]>dia[tank])
               min[ans]=dia[tank];
            tap=tank;
         }
         //printf("the diameter so far is %d\n",min[ans]);
         thetap[ans]=tap;
         ans++;
      }

   printf("%d\n",ans-1);
   for(i=1;i<ans;i++)
      printf("%d %d %d\n",thetank[i],thetap[i],min[i]);
      return 0;
}