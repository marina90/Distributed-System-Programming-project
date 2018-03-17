#!/usr/bin/env python
import sys


def reducer():
    current_count = 0
    current_word = ""
    for line in sys.stdin:
        split_line = line.split('\t')
        new_word = split_line[0]
        word_count = split_line[1]
        word_count = word_count.strip()
        if current_word == new_word:
            current_count += int(word_count)
        elif current_word is "":
            current_word = new_word
            current_count += int(word_count)
        else:
              sys.stdout.write("\t".join([current_word, str(current_count)]) + "\n")
              current_count = int(word_count)
              current_word = new_word
    sys.stdout.write("\t".join([current_word, str(current_count)]) + "\n")

if __name__ == '__main__':
    reducer()







