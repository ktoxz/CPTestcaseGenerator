""" Program name: Party
    Problem counter: #13
    Problem source: Codeforces
    Status: Completed
    Start date: 21/08/2023
    End date: 21/08/2023
    Rating: 900
    
"""

def main():

        n = int(input()) # number of employees
        
        emp = []   # take employee managers
        
        
        subs = []   # group employees with the same manager
        
        levels_above = {} # keeps track of what level each employee is
        
        
        # take 
        for _ in range(n):
            emp.append(int(input()))
        
        t_emp = tuple(emp)
        emp = list(set(emp))
        
        
        while len(emp) !=0:
            
            level = 1
            val = max(emp)
          
            levels_above[val] = 0
            temp_key = val
            
            #print(f"1. val = {val},\n len(emp) = {len(emp)}")
            
            emp.remove(val)
            
            run_once = False
            
            while val != -1:
                
                if val in levels_above.keys() and run_once:
                    
                    print("val in levels above")
                    print(f"val = {val}\nlevels_above = {levels_above[val]}")
                    print(f"levels = {level}")
                    
                    level = level + levels_above[val] -1
                    break
                else:
                    run_once = True
                    
                    print("In the else section")
                    print(f"temp_key = {temp_key}\nlevel = {level}")
                    
                    level = level + 1
                    val = t_emp[val-1]

                    #print(f"2.val = {val},\n len(emp) = {len(emp)}")

                    if val in emp:
                        emp.remove(val)
            
            #print(f"levels = {level}")
            subs.append(level)
            
            print(f"subs = {subs}")
            levels_above[temp_key] = subs[-1]
            
        print(max(subs))
                




if __name__ =="__main__":
    main()