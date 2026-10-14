#include <vector>

#include <list>

#include <map>

#include <set>

#include <queue>

#include <deque>

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

#include <ctime>

#include <string.h>



// defines

#define KhaledAshraf ios_base::sync_with_stdio(0);cin.tie(0);

#define endl '\n'

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



*/

void disp(lln H,lln M){

    if(H<10){

        cout<<0<<H;

    }

    else{

        cout<<H;

    }

    cout<<":";

    if(M<10){

        cout<<0<<M;

    }

    else{

        cout<<M;

    }



}





int main()

{

    //KhaledAshraf;

    lln H,M,reh=0;

    char a;

    lln X;

    cin>>H>>a>>M;

    X=H;

    reh+=X%10;

    reh*=10;

    X/=10;

    reh+=X;



    if(reh>M){

        while(reh>59){

            H++;

        reh=0;

        H%=24;

        X=H;

        reh+=X%10;

        reh*=10;

        X/=10;

        reh+=X;

        }

        disp(H,reh);

    }

    else{

        H++;

        reh=0;

        H%=24;

        X=H;

        reh+=X%10;

        reh*=10;

        X/=10;

        reh+=X;

        while(reh>59){

            H++;

        reh=0;

        H%=24;

        X=H;

        reh+=X%10;

        reh*=10;

        X/=10;

        reh+=X;

        }



        disp(H,reh);

    }





    return 0;

}