a,b,n=list(map(int,input().split()))
while n!=0:
    if n<a:
        print("1")
        break

    else:
         def get_fast_nod(a, n):
            if a < n:
                a, n = n, a

            while n != 0:
                a, n = n, a % n
            return a
    x=get_fast_nod(a,n)
    n=n-x
    if n<b:
        print("0")
        break
    else:

        def get_fast_nod(b, n):
            if b < n:
                b, n = n, b

            while n != 0:
                b, n = n, b % n
            return b
    y=get_fast_nod(b,n)
    n=n-y
    if n<a:
        print("1")
        break