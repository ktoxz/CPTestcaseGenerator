def main():
    n = int(input())

    a = list(input())
    b = list(input())

    
    count = 0
    for i in range(n):
        if a[i] == b[i]:
            continue
        if not n-i-1 > i:
            count += 1

        if a[n-i-1] == b[i]:
            a[i], a[n-i-1] = a[n-i-1], a[i]
        elif b[n-i-1] == a[i]:
            b[i], b[n-i-1] = b[n-i-1], b[i]
        elif a[i] == a[n-i-1]:
            b[i], a[n-i-1] = a[n-i-1], b[i]
        elif b[i] == b[n-i-1]:
            a[i], b[n-i-1] = b[n-i-1], a[i]
        else:
            count += 1

    print(count)


main()

# import sys, threading 
# if __name__ == '__main__':
#     sys.setrecursionlimit(1 << 30)
#     threading.stack_size(1 << 27)

#     main_thread = threading.Thread(target=main)
#     main_thread.start()
#     main_thread.join()