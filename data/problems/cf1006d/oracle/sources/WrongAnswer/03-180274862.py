from collections import Counter

def main():
    n = int(input())

    '''
    abccbba
    baabaaa
    '''

    a = input()
    b = input()

    count = 0
    for i in range(n//2):
        pos = Counter([a[i], a[n-i-1], b[i], b[n-i-1]])

        old = count
        if len(pos) == 4:
            count += 2
        elif len(pos) == 3 and a[i] == a[n-i-1]:
            count += 2
        elif len(pos) == 3 and b[i] == b[n-i-1]:
            count += 1
        elif len(pos) == 2 and ((a[i]==b[i] and a[n-i-1]!=b[n-i-1]) or a[i]!=b[i] and a[n-i-1]==b[n-i-1]):
            count += 1


    if n & 1:
        count += b[n//2] != a[n//2]
    
    print(count)

main()

# import sys, threading 
# if __name__ == '__main__':
#     sys.setrecursionlimit(1 << 30)
#     threading.stack_size(1 << 27)

#     main_thread = threading.Thread(target=main)
#     main_thread.start()
#     main_thread.join()