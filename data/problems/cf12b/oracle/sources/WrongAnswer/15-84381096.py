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
        alice = list(input())
        bob = int(input())

        sorted_alice = sorted(alice)
        smallest_number = []
        done = False

        for j in range(len(sorted_alice)):
            if int(sorted_alice[j]) != 0:
                break

        if j == len(sorted_alice):
            smallest_number = ["0"]
            done = True

        if not done:
            smallest_number = [sorted_alice[j]]
            sorted_alice[j] = -1

            for i in range(len(alice)):
                if int(sorted_alice[i]) < 0:
                    continue
                smallest_number.append(sorted_alice[i])

        smallest_number = int("".join(smallest_number))
        if smallest_number < bob:
            print("WRONG_ANSWER")
        else:
            print("OK")

B().solve()