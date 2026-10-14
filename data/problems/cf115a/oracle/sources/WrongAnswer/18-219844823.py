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
        subs = {}  # group employees with the same manager
        
        # take 
        for _ in range(n):
            emp.append(int(input()))

        for i in range(n):
            
            if not(emp[i] in subs.keys()):
                subs[emp[i]] = 1
            else:
                subs[emp[i]] = subs[emp[i]] + 1
   
        
        print(len(subs.keys()))




if __name__ =="__main__":
    main()