#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <climits>
#include <cfloat>
#include <map>
#include <utility>
#include <set>
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <algorithm>
#include <functional>
#include <sstream>
#include <complex>
#include <stack>
#include <queue>
#include <cstring>
using namespace std;
static const double EPS = 1e-5;
typedef long long ll;

int main()
{
   int i,n;
   long long count=0;
   long long m[100];
   cin >> n;
   for(i=0;i<n;i++)
	   cin>>m[i];
   for( i=0;i<n;i++)
   {
	   if (m[i]==0)
		   break;
	   else
	   {
		   count=count+m[i]+(m[i]-1)*i;

	   }
   }
      cout << count << endl;
   return 0;
}