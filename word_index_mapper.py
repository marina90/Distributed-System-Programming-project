#!/usr/bin/python
import sys


def mapper(line):
    res = ['1', line]
    sys.stdout.write('\t'.join(res))


def main():
    for line in sys.stdin:
        mapper(line)

if __name__ == '__main__':
    main()
