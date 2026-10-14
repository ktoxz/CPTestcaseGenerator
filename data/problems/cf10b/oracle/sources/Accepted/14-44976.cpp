#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cctype>
#include <string>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <limits.h>

using namespace std;






bool isFilled( int c[100][100] , int x , int y1 , int y2 ){
    for(int i = y1 ; i <= y2 ; i++ )
        if( c[x][i] == 1 )
            return true;
    return false;
}
void fillSeats( int c[100][100] , int x  , int y1 , int y2 ){
    for(int i = y1 ; i <= y2 ; i++)
        c[x][i]=1;
}
int main(){
    int n,k;
    cin>>n>>k;

    vector< pair<int , pair<int,int> > > ans;
    vector<int> req;
    for(int i = 0 ; i < n ; i++){
        int r;
        cin>>r;
        req.push_back(r);
    }

    int c[100][100];
    for(int i = 0 ; i < k ; i++)
        for(int j = 0; j < k ; j++)
            c[i][j]=0;

    for(int i = 0 ; i < req.size() ; i++){
        int rq = req[i];
        int xc,yc;
        xc = yc = k/2;

        int minf = INT_MAX,minyl,minyr,minx;

        for( int x = k-1 ; x >= 0 ; x-- ){
            for( int y = k-1 ; y >= rq-1 ; y--){
                int f1 = 0;
                int yl = y-rq+1;
                if(!isFilled(c,x,yl,y)){
                    for( int yr = y ; yr >= yl ; yr--){
                        f1 += abs(x-xc) + abs(yr-yc);
                    }
                    if(f1 <= minf){
                        minf = f1;
                        minyl = y-rq+1;
                        minyr = y;
                        minx = x;
                    }
                }
            }
        }
        if( minf == INT_MAX ){
            cout<<"-1\n";
        }
        else{
            fillSeats(c,minx,minyl,minyr);
            cout<<minx+1<<" "<<minyl+1<<" "<<minyr+1<<endl;
            //ans.push_back( mp( minx+1 , mp(minyl+1,minyr+1) ) );
        }
    }
    
    return 0;
}