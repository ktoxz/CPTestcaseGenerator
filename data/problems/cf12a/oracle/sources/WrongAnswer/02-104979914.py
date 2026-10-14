def main():
    s1 = input()
    s2 = input()
    s3 = input()
    if s1[0] + s2[0] + s3[0] == s3[2] + s2[2] + s1[2]:
        if s2[0] + s3[1] == s2[2] + s1[1] and s2[0] + s3[1] == s2[2] + s1[1]:
            if s3[0] == s1[2] and s1[0] == s3[2]:
                print("YES")
            else:
                print("NO")
                exit()
    else:
        print("NO")


if __name__ == '__main__':
    main()