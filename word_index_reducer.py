#!/usr/bin/python
import sys


def reducer():
    i = 0
    for line in sys.stdin:
        if line != '\n':
            split_line = line.split('\t')
            count = split_line[2].strip()
            key = split_line[1]
            val = str([i, int(count)])
            res = [key, val]
            sys.stdout.write('\t'.join(res) + '\n')
            i += 1


def main():
    reducer()


if __name__ == '__main__':
    main()
