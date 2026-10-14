def sol():
    n,m,h = (int(x) for x in input().split())
    studs_dept = [int(x) for x in input().split()]
    if sum(studs_dept) <n:
        return -1
    studs_herrsdept = studs_dept[h-1]-1
    if studs_herrsdept <= 0:
        return 0
    if sum(studs_dept) == n:
        return 1
    # acombination formed by herr and his dept only
    def inner_combination(a):
        if a < 2:
            return 0
        if a == 2:
            return 1
        return sum([i for i in range(a)])
    num_other_dept = sum(studs_dept) - studs_herrsdept-1
    def mixed_combination(inner,outer):  #the combination formed by inner mixed with outer
        return inner*outer
    def outer_combination(a):
        if a < 2:
            return 0
        if a == 2:
            return 1
        return sum([i for i in range(a)])
    inner_combine = inner_combination(studs_herrsdept)
    #print(inner_combine)
    mixed_combine = mixed_combination(studs_herrsdept,num_other_dept)
    #print(mixed_combine)
    outer_combine = outer_combination(num_other_dept)
    #print(outer_combine)
    return (inner_combine+mixed_combine)/(inner_combine+outer_combine+mixed_combine)
print(sol())