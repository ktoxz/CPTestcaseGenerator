#include <iostream>

#include <iomanip>

#include <vector>

#include <list>

#include <map>

#include <set>

#include <queue>

#include <deque>

#include <stack>

#include <string>

#include <string.h>

#include <math.h>

#include <cmath>

#include <algorithm>

#include <bitset>

#include <functional>

#include <numeric>

#include <utility>

#include <sstream>

#include <cstdio>

#include <cstdlib>

#include <ctime>





// defines

#define modulo 1000000007

#define pi 3.1415926535897932384



typedef long long int lln;









//to be able to use to_string  patch::to_string("char or string")



namespace patch

{

    template < typename T > std::string to_string( const T& n )

    {

        std::ostringstream stm ;

        stm << n ;

        return stm.str() ;

    }

}



















using namespace std;



/*******************************************/





/*

                    ya mas2la zebala accept b2a



                               O_O



                        $$$$$$$$$$$$$$$

      $ $             $$$$$$$$$$$$$$$$$$$$$          $ $

      $ $  $         $$$$$$$$$$$$$$$$$$$$$$$$     $  $ $

    $ $ $ $        $$$$$$    $$$$$$    $$$$$$      $ $ $ $

     $$$$$        $$$$$$      $$$$      $$$$$$$     $$$$$

     $$$$$$$$    $$$$$$$      $$$$      $$$$$$$$ $$$$$$$$

       $$$      $$$$$$$$$    $$$$$$    $$$$$$$$$$   $$$

        $$    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    $$

         $     $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$  $$   $

          $$$$$$$$  $$$$$$$$$$$$$$$$$$$$$$$$  $$$$$$

               $$$  $$$$$$$$$$$$$$$$$$$$$$$$  $$$

                $$$     $$$$$$$$$$$$$$$$     $$

                 $$        $$$$$$$$$$       $$

                  $$$                       $

                    $$    $$$$$$$$$$$      $

                     $$$     $$$$$$$$$$$  $

                        $$$     $$$$$$$$$$

                           $$$$$  $$$$$$$$$

                                   $$$$$$$

                                     $$$$



                          Khaled Ashraf

*/









int main()

{

    ios_base::sync_with_stdio(0);

	cin.tie(0);



    int N,D,arr[3000],res=0,per1=0,per2=0;

    cin>>N>>D;

    for(int i=0;i<N;cin>>arr[i++]);

    for(int i=1;i<N;i++){

        if(arr[i-1]>=arr[i]){

            per1=arr[i-1]/D;

            per2=arr[i]/D;

            arr[i]+=(per1-per2)*D;

            res+=per1-per2;

            if(arr[i-1]>=arr[i]){

                arr[i]+=D;

                res+=1;

            }



        }

    }

   cout<<res;



    return 0;

}