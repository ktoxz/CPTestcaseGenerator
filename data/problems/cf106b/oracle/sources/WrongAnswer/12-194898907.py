def compare(laptop1: list, laptop2: list):
    if laptop1[0] < laptop2[0] and laptop1[1] < laptop2[1] and laptop1[2] < laptop2[2]:
        return True
    else:
        return False

def main():
    laptop = []
    laptops = []
    n = int(input())
    for g in range(n):
        laptops = input().split()
        laptop.append(laptops)
    minimum = 10000
    index = 0
    for i in range(0, len(laptop)):
        for j in range(0, len(laptop)):
            if not compare(laptop[i], laptop[j]):
                if int(laptop[i][3]) < minimum:
                    minimum = int(laptop[i][3])
                    index = i
    print(index)



if __name__ == '__main__':
    main()