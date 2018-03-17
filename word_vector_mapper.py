#!/usr/bin/python
import sys

gold_words = {}


def build_other(sngram):
    other = sngram[0]
    other += '+'
    other += sngram[2]
    return other


def mapper(line):
    split_line=line.split('\t')
    word=split_line[0]
    others=split_line[1]
    amount = split_line[2]
    dummy=gold_words.get(word,"notingoldwords")
    if(dummy!="notingoldwords"):
        other_words = others.split(' ')
        other_words = map(lambda sngram: sngram.split('/'), other_words)
        other_words = filter(lambda item: item[0].isalpha() and item[0]!=word , other_words)
        other_words = map(lambda sngram: build_other(sngram), other_words)
        for other in other_words:
            res = [word, other, amount]
            sys.stdout.write('\t'.join(res) + '\n')

def main():
    global gold_words
    with open('./input2.txt') as file:
        for line in file:
            word1,word2,flag = line.split('\t')
            gold_words[word1]=0
            gold_words[word2]=0
    for line in sys.stdin:
		if not line == "" and not line == '\t\n' and not line == '\n\t' and not line == '\n\tat':
			mapper(line)


if __name__ == '__main__':
    main()
