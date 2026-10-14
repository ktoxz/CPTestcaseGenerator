class Heap:
    def __init__(self):
        self.list = [(0, 0)]

    def insert(self, ele):
        pos = len(self.list)
        self.list.append(ele)
        while pos > 1 and self.list[pos][-1] < self.list[pos // 2][-1]:
            self.list[pos], self.list[pos // 2] = self.list[pos // 2], self.list[pos]
            pos = pos // 2

    def extract(self):
        ele = self.list[1]
        self.list[1] = self.list[-1]
        self.list = self.list[:-1]
        pos = 1
        while pos * 2 + 1 <= len(self.list):
            if pos * 2 + 1 == len(self.list):
                smallest = pos * 2
            else:
                left, right = self.list[pos * 2][-1], self.list[pos * 2 + 1][-1]
                smallest = pos * 2 if left < right else pos * 2 + 1
            if self.list[smallest][-1] < self.list[pos][-1]:
                self.list[smallest], self.list[pos] = self.list[pos], self.list[smallest]
                pos = smallest
            else:
                break
        return ele

    def peek(self):
        return self.list[1]

    def empty(self):
        return len(self.list) == 1


def main():
    N, K = map(int, input().split())
    M = tuple(map(int, input().split()))

    center = K // 2 + 1
    heap1, heap2 = Heap(), Heap()
    for i in range(1, K + 1):
        if i <= center:
            heap1.insert((i, center - i))
        else:
            heap1.insert((i, i - center + 0.002 * i))


    for i in range(N):
        if heap1.empty() and heap2.empty():
            print(-1)

        elif heap2.empty():
            row = heap1.extract()[0]
            start = center - M[i] // 2
            end = center + (M[i] - 1) // 2
            if row <= center:
                if start > 1:
                    heap2.insert((row, start - 1, center - row + center - start + 0.001 * row))
                if end < K:
                    heap2.insert((row, end + 1, center - row + end - center + 0.001 * row + 0.0005))
            else:
                if start > 1:
                    heap2.insert((row, start - 1, row - center + center - start + 0.001 * row))
                if end < K:
                    heap2.insert((row, end + 1, row - center + end - center + 0.001 * row + 0.0005))
            print(row, start, end)

        elif heap1.empty():
            a = []
            x = None
            while not heap2.empty():
                b = heap2.extract()
                if b[1] < center:
                    if b[1] < M[i]:
                        a.append(b)
                    else:
                        row = b[0]
                        start = b[1] - M[i] + 1
                        end = b[1]
                        print(row, start, end)
                        if start > 1:
                            if row <= center:
                                x = (row, start - 1, center - row + center - start + 0.001 * row)
                            else:
                                x = (row, start - 1, row - center + center - start + 0.001 * row)
                        break
                else:
                    if K - b[1] + 1 < M[i]:
                        a.append(b)
                    else:
                        row = b[0]
                        start = b[1]
                        end = b[1] + M[i] - 1
                        print(row, start, end)
                        if end < K:
                            if row <= center:
                                x = (row, end + 1, center - row + end - center + 0.001 * row + 0.0005)
                            else:
                                x = (row, end + 1, row - center + end - center + 0.001 * row + 0.0005)
                        break
            else:
                print(-1)
            while a:
                heap2.insert(a.pop())
            if x:
                heap2.insert(x)

        else:
            opt1 = heap1.peek()
            opt1_dist = opt1[1] + (0 if M[i] % 2 else 0.5)
            a = []
            x = None
            opt2_dist = 999
            while not heap2.empty():
                opt2 = heap2.extract()
                if opt2[1] < center:
                    if opt2[1] < M[i]:
                        a.append(opt2)
                    else:
                        opt2_dist = opt2[1] + (M[i] - 1) / 2
                        break
                else:
                    if K - opt2[1] + 1 < M[i]:
                        a.append(opt2)
                    else:
                        opt2_dist = opt2[1] + (M[i] - 1) / 2
                        break
            if opt1_dist < opt2_dist:
                row = heap1.extract()[0]
                start = center - M[i] // 2
                end = center + (M[i] - 1) // 2
                if row <= center:
                    if start > 1:
                        heap2.insert((row, start - 1, center - row + center - start + 0.001 * row))
                    if end < K:
                        heap2.insert((row, end + 1, center - row + end - center + 0.001 * row + 0.0005))
                else:
                    if start > 1:
                        heap2.insert((row, start - 1, row - center + center - start + 0.001 * row))
                    if end < K:
                        heap2.insert((row, end + 1, row - center + end - center + 0.001 * row + 0.0005))
                print(row, start, end)
                while a:
                    heap2.insert(a.pop())
                if opt2_dist != 999:
                    heap2.insert(opt2)
            else:
                if opt2[1] < center:
                    row = opt2[0]
                    start = opt2[1] - M[i] + 1
                    end = opt2[1]
                    print(row, start, end)
                    if start > 1:
                        if row <= center:
                            x = (row, start - 1, center - row + center - start + 0.001 * row)
                        else:
                            x = (row, start - 1, row - center + center - start + 0.001 * row)
                else:
                    row = opt2[0]
                    start = opt2[1]
                    end = opt2[1] + M[i] - 1
                    print(row, start, end)
                    if end < K:
                        if row <= center:
                            x = (row, end + 1, center - row + end - center + 0.001 * row + 0.0005)
                        else:
                            x = (row, end + 1, row - center + end - center + 0.001 * row + 0.0005)
                while a:
                    heap2.insert(a.pop())
                if x:
                    heap2.insert(x)
        pass


if __name__ == "__main__":
    main()