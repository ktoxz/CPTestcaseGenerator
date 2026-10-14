// C

# include <stdio.h>
# include <cstring>

using namespace std;

const int N = 110;
const int M = 33;

int p [N], q [N];
char s [N][M], t [M];
int n, m, sum, k;

int main ()
{
# ifndef ONLINE_JUDGE
   freopen ("C.TXT", "rt", stdin);
   freopen ("C.OUT", "wt", stdout);
# endif

   int i, j, x, n2;
   bool ok;

   scanf ("%d %d", &n, &m);

   for ( j=0; j < n; j++ )
      scanf ("%d", &p [j]);

   gets (s [0]);
   for ( j=0; j < m; j++ )
   {
      gets (t);
      for ( i=0, ok=false; i < k; i++ )
         if ( ! strcmp (t, s [i]) )
            { ok = true; break; }

      if ( ok )
         q [i] ++;
      else
      {
         q [i] = 1, k++;
         strcpy (s [i], t);
      }
   }

   for ( j=0; j < n-1; j++ )
      for ( i=0; i < n-j-1; i++ )
         if ( p [i] > p [i+1] )
            x = p [i], p [i] = p [i+1], p [i+1] = x;

   for ( j=0; j < k-1; j++ )
      for ( i=0; i < k-j-1; i++ )
         if ( q [i] < q [i+1] )
            x = q [i], q [i] = q [i+1], q [i+1] = x;

   for ( j=0; j < N; j++ )
      sum += p [j]*q [j];

   printf ("%d ", sum);

   for ( i=0, n2=(n+1)/2; i < n2; i++ )
      x = p [i], p [i] = p [n-1-i], p [n-1-i] = x;

   for ( j=0, sum=0; j < N; j++ )
      sum += p [j]*q [j];

   printf ("%d", sum);

/*
   printf ("\nn=%d m=%d\n", n, m);

   for ( j=0; j < n; j++ )
      printf (" %d", p [j]);
   printf ("\nk=%d\n", k);
   for ( j=0; j < k; j++ )
      printf ("%s   %d\n", s [j], q [j]);
   printf ("\n");
   for ( j=0; j < n; j++ )
      printf (" %d", p [j]);
   printf ("\n");
*/
   return 0;
}