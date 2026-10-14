class A:

    def rotate_keypad(self, keypad):
        reversed_rows = list(reversed(keypad))
        return ["".join(list(reversed(x))) for x in reversed_rows]

    def solve(self):
        keypad = [input(), input(), input()]
        if keypad == self.rotate_keypad(keypad):
            print("YES")
        else:
            print("NO")

class B:

    def solve(self):
        alice = input()
        bob = input()

        if bob[0] == '0' and alice[0] != '0':
            print("WRONG_ANSWER")
            return
        elif bob[0] == '0' and alice[0] == '0' and len(bob) != 1:
            print("WRONG_ANSWER")
            return


        bob = int(bob)

        from itertools import permutations

        smallest = int(alice)
        if smallest == 0:
            if bob == 0:
                print("OK")
            else:
                print("WRONG_ANSWER")
        else:
            smallest = min([int("".join(list(perm))) for perm in permutations(sorted(alice)) if perm[0] != '0'])
            if smallest == bob:
                print("OK")
            else:
                print("WRONG_ANSWER")

class C:

    def solve(self):
        [n, m] = [int(x) for x in input().split(" ")]
        prices = sorted([int(x) for x in input().split(" ")])

        fruits = []
        for i in range(m):
            fruits.append(input())

        from collections import Counter
        frequent_fruits = [f for (f, p) in Counter(fruits).most_common()]

        price_assignment = {}
        for f, p in zip(frequent_fruits, prices):
            price_assignment[f] = p

        smallest_price = sum([price_assignment[f] for f in fruits])

        for f, p in zip(frequent_fruits, list(reversed(prices))):
            price_assignment[f] = p

        largest_price = sum([price_assignment[f] for f in fruits])

        print("{} {}".format(smallest_price, largest_price))

class D:

    def solve(self):
        n = int(input())
        ladies = []

        for x in input().split(" "):
            ladies.append([x])

        for i, x in enumerate(input().split(" ")):
            ladies[i].append(x)

        for i, x in enumerate(input().split(" ")):
            ladies[i].append(x)

        self_murderers = 0
        for i in range(n):
            if any([ladies[i][0] < ladies[x][0] and\
                    ladies[i][1] < ladies[x][1] and\
                    ladies[i][2] < ladies[x][2] for x in range(n) if x != i]):
                self_murderers += 1

        print(self_murderers)

class E:

    def generate_matrix(self, i, j, n, matrix):
        if i == j:
            matrix[i][j] = 0
        else:
            if matrix[i][j] == 0:
                dictionary = {}
                for e in matrix[i]:
                    dictionary[e] = True
                for e in matrix[j]:
                    dictionary[e] = True
                for index in range(n):
                    if index not in dictionary:
                        matrix[i][j] = index
                        matrix[j][i] = index
                        break

    def solve(self):
        n = int(input())

        matrix = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(n):
                self.generate_matrix(i, j, n, matrix)
        transponse = list(map(list, zip(*matrix)))
        if matrix != transponse:
            raise Exception("FC")
        print("\n".join([" ".join([str(y) for y in x]) for x in matrix]))

B().solve()