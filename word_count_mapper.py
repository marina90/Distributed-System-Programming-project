#!/usr/bin/env python
import sys


def print_other_words(data, count):
    count_of_all_words = 0
    for i in data:
        if i[0] == "" or i[0] == " ":
            i[0] = "/"
        if i[0].isalpha():
            sys.stdout.write("\t".join([i[0] + "+" + i[1], str(count)]) + "\n")
            count_of_all_words += int(count)
    return count_of_all_words


def mapper():
    current_count = 1
    current_word = ""
    count_of_all_words = 0
    for line in sys.stdin:
        split_line = line.split('\t')
        word = split_line[0]
        other_words = split_line[1].split(' ')
        other_words = map(lambda x: [x.split('/')[0], x.split('/')[2]], other_words)
        if word.isalpha():
            if current_word == word:
                current_count += int(split_line[2])
                count_of_all_words += print_other_words(other_words, split_line[2])
            elif current_word is "":
                    current_count = int(split_line[2])
                    current_word = word
                    count_of_all_words += print_other_words(other_words, split_line[2])
            else:
                count_of_all_words += current_count
                sys.stdout.write("\t".join([current_word,str(current_count)])+"\n")
                count_of_all_words += print_other_words(other_words, split_line[2])
                current_count = int(split_line[2])
                current_word = word
    sys.stdout.write("\t".join([current_word, str(current_count)]) + "\n")
    count_of_all_words += current_count
    sys.stdout.write("\t".join(["count_of_all_words", str(count_of_all_words)]) + "\n")


def main():
    mapper()

if __name__ == '__main__':
    main()