#include <stdio.h>
#define Nmax 2005

int n, k, x, mlt, i, nr;
int T[Nmax];

int main()
{
  //freopen ("fis.in", "r", stdin);
  scanf ("%d %d\n", &n, &k);
  for (i=0; i<n; i++)
    scanf ("%d ", &T[i]);
  nr=0;
  for (i=1; i<n; i++)
    if (T[i-1]>T[i])
    {
      x=T[i-1]-T[i];
      nr+=x/k;
      mlt=x/k;
      nr++;
      mlt++;
      T[i]+=k*mlt;
    }
    else
      if (T[i-1]==T[i])
      {
        T[i]+=k;
        nr++;
      }
  printf ("%d\n", nr);
  return 0;
}