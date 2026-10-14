#include<stdio.h>

#define MAXK 100

#define ABS(x) ((x)>0?(x):-(x))

int n, k, m;

bool a[MAXK][MAXK];

int t, b;
int bx, by;

int p;

int x, y; 

int i;

int main()
{
 
 scanf("%d%d", &n, &k);
 
 for(i = 0; i < n; i++)
 {
  scanf("%d", &m); 
  
  b = -1;
  
  for(y = 0; y < k; y++)
  {
   t = 0;
   p = 0;
   
   for(x = 0; x < k; x++)
    if(!a[x][y])
    {
     if(p<m)
      p++;
     else
      t -= ABS(x - m - k/2) + ABS(y - k/2);
     
     t += ABS(x - k/2) + ABS(y - k/2);
     
     if(p == m && (t < b || b == -1))
     {
      b = t;
      bx = x; 
      by = y;
     }
    }   
    else
    {
     p = 0;
     t = 0;
    }  
   }
   if(b == -1)
    printf("-1\n");
   else
   {
    for(x = 0; x < m; x++) 
     a[bx - x][by] = true;
      
    printf("%d %d %d\n", by+1, bx - m + 2, bx + 1);
   }
 }
 
 getchar();
 getchar();
 
 return 0;
}