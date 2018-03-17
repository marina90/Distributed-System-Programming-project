#!/usr/bin/python
import sys
from ast import literal_eval
from math import log
import operator as op
from rsa._compat import MAX_INT
from gc import collect


count_of_all_words = 0
count_pairs = 0
counts_map = {}

def ncr(n, r):
    try:
        r = min(r, n-r)
        if r == 0:
            return 1
        numer = reduce(op.mul, xrange(n, n-r, -1))
        denom = reduce(op.mul, xrange(1, r+1))
        return numer//denom
    except:
        return MAX_INT


def other_amount(other):
    ans = int(other[1])
    return max(ans, 1)


def index_to_count(word):
    global counts_map
    try:
        index_count = counts_map[word]
        index_count = literal_eval(index_count)
    except KeyError:
        index_count = [-1, 1000]

    return index_count


def mapper(line):    	
	split_line = line.split('\t')
	word = split_line[0]
	others_vector = split_line[1]
	line = ''
	others_vector = literal_eval(others_vector)
	others_vector.sort()
	vector_amount = map(lambda other: other_amount(other), others_vector)
	other_words = map(lambda other: other[0], others_vector)	
	other_words = map(lambda x: index_to_count(x), other_words)
	others_vector = ''
	collect()
	first_vector = []
	for i in xrange(len(vector_amount)):
		new_pair = other_words[i][:]
		new_pair[1] = vector_amount[i]
		first_vector.append(new_pair[:])
	word_amount = float(index_to_count(word)[1])
	second_vector = map(lambda x: round(float(x[1]) / word_amount, 6), first_vector)
	for i in xrange(len(second_vector)):
		new_pair = other_words[i][:]
		new_pair[1] = second_vector[i]
		second_vector[i] = new_pair[:]
	vector_amount = map(lambda x: round(float(x) / count_pairs, 6), vector_amount)
	third_vector = []
	fourth_vector = []
	division = word_amount / count_of_all_words
	for i in xrange(len(vector_amount)):
		den2 = float(other_words[i][1]) / count_of_all_words
		den = division*den2
		new_pair = other_words[i][:]
		if vector_amount[i] == 0:
			vector_amount[i] = 0.000001
		new_pair[1] = round(log((vector_amount[i]/den), 2), 6)
		third_vector.append(new_pair[:])
		amount = vector_amount[i] - den
		den = den ** 0.5
		new_pair[1] = round(amount / den, 6)
		fourth_vector.append(new_pair[:])
	val = [first_vector, second_vector, third_vector, fourth_vector]	
	sys.stdout.write('\t'.join([word, str(val)]) + '\n')       
	collect()
        


def main():
    global counts_map
    global count_of_all_words
    global count_pairs
    with open('input.txt') as file:
        for line in file:
            (key, val) = line.split('\t')
            counts_map[key] = val
    count_of_all_words = index_to_count('count_of_all_words')[1]
    count_pairs = ncr(count_of_all_words, 2)
    collect()
	for line in sys.stdin:
		mapper(line)
   


if __name__ == '__main__':
    main()
