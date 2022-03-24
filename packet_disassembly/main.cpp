#include <iostream>
#include <fstream>
#include <cstdio>
#include <cassert>
#include <cstdlib>

using namespace std ;







int main(int argc, const char * argv[]) {
    
    int length = 2 ;
    
    string line;
    char c ;
    
    ifstream myfile ("MarketDataLog_20220215_23615.log");
    if (myfile.is_open())
    {
        ofstream output("export_c++.txt") ;
        
        for (int i = 0; i < length; i++)
        {
            myfile.get(c) ;
            
            //printf("%02x ", (unsigned char)c) ;
            
            
            bitset<8> x(c);
            cout << x[6] << ' ';
            if (/*c == 0b01001101*/ c == 0x4d) {
                cout << "true" << endl ;
            }
            else
            {
                cout << "false" << endl ;
            }
            
            for (int j = 0; j < 8; j++)
            {
                output << ((c >> j) & 1);
            }
        }
        
        
        
        output.close() ;
        myfile.close();
    }

    else cout << "Unable to open file\n";
        

    
    
    
    
    
    
    
    
    
    return 0 ;
    
}
