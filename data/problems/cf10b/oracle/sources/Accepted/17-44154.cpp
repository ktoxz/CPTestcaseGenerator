#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <set>
#include <cmath>
#include <sstream>
#include <utility>
#include <cstring>
#include <stdio.h>
using namespace std;
#define INF          (1 << 30)
int main()
{
   //freopen("entrada.txt","r",stdin);
   //freopen("salida.txt","w",stdout);
   int M, k;
   cin >> M >> k;
   int people[M];
   for (int i = 0; i < M; ++i)
      cin >> people[i];
   int medio = k/2 +1;
   //INICIO
   bool ocupados[k+10][k+10];
   memset (ocupados, false, sizeof (ocupados));
   for (int turno = 0; turno < M; ++turno)
   {
      int rta[k+10][k+10];
      int minimo = INF, minimo_x, minimo_y;
      bool sin_solucion = true;
      int personas = people[turno];
      memset (rta, 0, sizeof (rta));
      for (int x = 1; x <= k; ++x)
      {
         for (int y = 1; y+personas-1 <= k; ++y)
         {
            int& ref = rta[x][y];
            for (int h = y; h < y+personas; ++h)
            {
               if (ocupados[x][h])
               {
                  ref = INF;
                  break;
               }
               ref += abs (medio - x) + abs (medio - h);
            }
            if (ref < minimo)
            {
               sin_solucion = false;
               minimo = ref;
               minimo_x = x;
               minimo_y = y;
            }
         }
      }
      if (sin_solucion)
         cout << "-1\n";
      else
      {
         cout << minimo_x << " " << minimo_y << " " << minimo_y + personas-1 << endl;
         for (int y = minimo_y; y < minimo_y + personas; ++y)
            ocupados[minimo_x][y] = true;
      }
   }
   //FIN
   return 0;
}