#!/usr/bin/python
import sys

index = 0

def main():
    reducer()


def reducer():
    curr = ""
    word_pairs_map={}
    for line in sys.stdin:
        if not line == "" and not line == '\t\n' and not line =="\t" and not line == "\n" and not line == " ":
            split_line = line.split('\t')
            left_word = split_line[0]
            right_word = split_line[1]
            data_vector = split_line[3]
            if (curr==""):
                curr=left_word
                word_pairs_map[right_word]=data_vector.strip()
            elif (curr==left_word):
                no_key=word_pairs_map.get(right_word,"key_not_found")
                if(no_key == "key_not_found"):
                    word_pairs_map[right_word]=data_vector
                else:
                    data_to_send=[left_word,right_word,split_line[2],str(data_vector.strip()),str(word_pairs_map[right_word])]
                    print "\t".join(data_to_send)
            else:
                curr=left_word
                word_pairs_map={}
                word_pairs_map[right_word]=data_vector.strip()


if __name__ == '__main__':
    main()