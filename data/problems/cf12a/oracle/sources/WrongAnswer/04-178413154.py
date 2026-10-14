# Author <<< MAVERICK >>>
import os, sys, math
ii  = lambda : int(input())                           
si  = lambda : input()                               
mi  = lambda : map(int,input().strip().split(" "))   
msi = lambda : map(str,input().strip().split(" "))   
li  = lambda : list(mi())                            
lsi = lambda : list(msi())                           
iseven = lambda num : num%2==0                       
isodd = lambda num : num%2==1                        

class Maverick:
    def __init__(self) -> None:
        self.counter,self.summation,self.store,self.dick,self.alphabets = 0,0,[],{},"abcdefghijklmnopqrstuvwxyz"
    def process(self) -> None:
        try:
            import master
            master.Verdict().read(); self.solve(); master.Verdict().compare()
        except (FileNotFoundError, ModuleNotFoundError): self.solve()
    def clearAll(self): self.counter, self.summation = 0,0; self.dick.clear(); self.store.clear()
    def solve(self) -> None:

        s1 = si()
        s2 = si()
        s3 = si()

        if s1==s3[::-1]: print(f"YES",end="\n")
        else: print(f"NO",end="\n")


if __name__ == "__main__": Maverick().process()