# CodeForces : 105A Transmigration
if __name__ == "__main__": 
    n,m,k=map(float,input().split())
    n,m,k=int(n),int(m), round(k,2)
    skills=[]
    points=[]
    for i in range (n):
        a=input().split()
        level= (int(a[1])*k)
        if level>100:
            skills.append(a[0])
            points.append(int(level))
    for i in range (m):
        a=input()
        if a not in skills:
            skills.append(a)
            points.append(0)
    print(len(skills))
    [print(skills[i],points[i]) for i in range (len(skills))]