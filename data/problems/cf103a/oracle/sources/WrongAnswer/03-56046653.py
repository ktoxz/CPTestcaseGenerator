class CodeforcesTask103ASolution:
    def __init__(self):
        self.result = ''
        self.questions = []

    def read_input(self):
        input()
        self.questions = [int(x) for x in input().split(" ")]

    def process_task(self):
        clicks = 0
        for i, question in enumerate(self.questions):
            if question > 1:
                clicks += i
                clicks += question
            else:
                clicks += 1

        self.result = str(clicks)

    def get_result(self):
        return self.result


if __name__ == "__main__":
    Solution = CodeforcesTask103ASolution()
    Solution.read_input()
    Solution.process_task()
    print(Solution.get_result())