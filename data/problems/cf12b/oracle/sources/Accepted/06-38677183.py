def main():
    curr = list(sorted(list(input())))
    test = input()

    idx = 0

    for i, nbr in enumerate(curr):
        if nbr != '0':
            idx = i
            break

    tmp = curr[idx]
    curr.remove(tmp)
    curr.insert(0, tmp)

    print("OK" if ''.join(curr) == test else "WRONG_ANSWER")


if __name__ == "__main__":
    main()