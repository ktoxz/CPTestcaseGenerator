def is_outdated(laptop1, laptop2):
    return laptop1[0] < laptop2[0] and laptop1[1] < laptop2[1] and laptop1[2] < laptop2[2]

def find_suitable_laptop(laptops):
    n = len(laptops)
    suitable_laptops = []
    
    for i in range(n):
        is_current_laptop_suitable = True
        
        for j in range(n):
            if i != j and is_outdated(laptops[i], laptops[j]):
                is_current_laptop_suitable = False
                break
        
        if is_current_laptop_suitable:
            suitable_laptops.append(laptops[i])

    return min(suitable_laptops, key=lambda x: x[3])[3]

def main():
    n = int(input())
    laptops = [tuple(map(int, input().split())) for _ in range(n)]
    result = find_suitable_laptop(laptops)
    print(result)

if __name__ == "__main__":
    main()