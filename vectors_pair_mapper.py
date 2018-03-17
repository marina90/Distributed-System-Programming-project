#!/usr/bin/python
import sys
import ast

data=[]

def main():
    with open ("input3.txt") as file:
        for line in file:
            if not line == "" and not line == '\t\n' and not line == "\n" and not line == " " :
                line=line.strip()
                data.append(line.split('\t'))

    mapper()


def mapper ():
    for line in sys.stdin:
        if not line == "" and not line == '\t\n' and not line == "\n" and not line == " ":
            split_line = line.split('\t')
            word_value = split_line[0]
            words_vector = split_line[1]
            words_vector = ast.literal_eval(words_vector)
            for i in range(4):
              words_vector[i].sort()
            for item in data:
                if (item[0]==word_value or item[1]==word_value):
                    result = [item[0], item[1], item[2].strip(), str(words_vector)]
                    print '\t'.join(result)


if __name__ == '__main__':
    main()