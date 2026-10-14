def fun(n):
    if 0<=n<=9:
        return n
    else:
        return (n%10)+fun(n/10)

def main():
    n = int(input())
    count = 0
    if 0<=n<=9:
        count = 0
    while n>9:
        n = fun(n)
        count +=1
    print(count)
    
if __name__ == "__main__":
    main()