#! /usr/bin/env python3

import itertools
import sys


def main():
    solve()


def solve():
    data = sys.stdin.readlines()
    p1, p2, p3, t1, t2, intervals = parse(data)
    consumption = calc_consumption(p1, p2, p3, t1, t2, intervals)
    print(consumption)


def parse(data):
    _, p1, p2, p3, t1, t2 = tuple(int(s) for s in data[0].split())
    intervals = tuple(parse_line(line) for line in data[1:])
    return p1, p2, p3, t1, t2, intervals


def parse_line(line):
    ls, rs = line.split()
    return (int(ls), int(rs))


def calc_consumption(p1, p2, p3, t1, t2, intervals):
    consumption = 0
    cur_time = intervals[0][0]
    for l, r in intervals:
        consumption += calc_idle_consumption(l - cur_time, p1, p2, p3, t1, t2)
        consumption += (r - l) * p1
        cur_time = r

    return consumption


def calc_idle_consumption(duration, p1, p2, p3, t1, t2):
    dur = min(duration, t1)
    consumption = dur * p1
    duration -= dur

    dur = min(duration, t2)
    consumption += dur * p2
    duration -= dur

    return consumption + duration * p3
    

if __name__ == '__main__':
    main()