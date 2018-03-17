#!/usr/bin/python
import sys
import ast
import math

data={}

def main():    
    for line in sys.stdin:
	if not line == "" and not line == '\t\n' and not line == "\n" :
	    mapper(line)


def mapper (line):    
    split_line = line.split("\t")
    word1=split_line[0]
    word2=split_line[1]
    flag=split_line[2]
    vector_array1 = split_line[3]
    vector_array2 = split_line[4]
    vector_array1 = ast.literal_eval(vector_array1)
    vector_array2 = ast.literal_eval(vector_array2)
    vector1_size= len(vector_array1[1])
    vector2_size = len(vector_array2[1])
    sim_array = []

    for idx, val in enumerate(vector_array1):
        manhatten=0
        i=0
        j=0
        while(i<vector1_size and j<vector2_size):
            if(vector_array1[idx][i][0]==vector_array2[idx][j][0]):
                manhatten += abs(vector_array1[idx][i][1] - vector_array2[idx][j][1])
                i+=1
                j+=1
            elif (vector_array1[idx][i][0]<vector_array2[idx][j][0]):
                manhatten += abs(vector_array1[idx][i][1])
                i+=1
            else:
                manhatten += abs(vector_array2[idx][j][1])
                j+=1
        while(i<vector1_size):
            manhatten += abs(vector_array1[idx][i][1])
            i+=1
        while(j<vector2_size):
            manhatten += abs(vector_array2[idx][j][1])
            j+=1
        sim_array.append(manhatten)

    for idx, val in enumerate(vector_array1):
        euclidean=0
        i = 0
        j = 0
        while (i < vector1_size and j < vector2_size):
            if (vector_array1[idx][i][0] == vector_array2[idx][j][0]):
                euclidean += pow(vector_array1[idx][i][1] - vector_array2[idx][j][1], 2)
                i+=1
                j+=1
            elif (vector_array1[idx][i][0] < vector_array2[idx][j][0]):
                euclidean += pow(vector_array1[idx][i][1],2)
                i+=1
            else:
                euclidean += pow(vector_array2[idx][j][1], 2)
                j+=1
        while (i < vector1_size):
            euclidean += pow(vector_array1[idx][i][1], 2)
            i += 1
        while (j < vector2_size):
            euclidean += pow(vector_array2[idx][j][1], 2)
            j += 1
        euclidean = math.sqrt(euclidean)
        sim_array.append(euclidean)

    for idx, val in enumerate(vector_array1):
        cosine_numerator = 0
        cosine_denominator1 = 0
        cosine_denominator2 = 0
        i=0
        j=0
        while (i < vector1_size and j < vector2_size):
            if (vector_array1[idx][i][0] == vector_array2[idx][j][0]):
                cosine_numerator += (vector_array1[idx][i][1] * vector_array2[idx][j][1])
                cosine_denominator1 += pow(vector_array1[idx][i][1], 2)
                cosine_denominator2 += pow(vector_array2[idx][j][1], 2)
                i+=1
                j+=1
            elif (vector_array1[idx][i][0] < vector_array2[idx][j][0]):
                cosine_denominator1 += pow(vector_array1[idx][i][1], 2)
                i+=1
            else:
                cosine_denominator2 += pow(vector_array2[idx][j][1], 2)
                j+=1
        while (i < vector1_size):
            cosine_denominator1 += pow(vector_array1[idx][i][1], 2)
            i += 1
        while (j < vector2_size):
            cosine_denominator2 += pow(vector_array2[idx][j][1], 2)
            j += 1
        cosine_denominator1 = math.sqrt(cosine_denominator1)
        cosine_denominator2 = math.sqrt(cosine_denominator2)
        sim_array.append(cosine_numerator / (cosine_denominator1 * cosine_denominator2))


    for idx, val in enumerate(vector_array1):
        jaccard_numerator = 0
        jaccard_denominator = 0
        i=0
        j=0
        while (i < vector1_size and j < vector2_size):
            if (vector_array1[idx][i][0] == vector_array2[idx][j][0]):
                jaccard_numerator += min(vector_array1[idx][i][1], vector_array2[idx][j][1])
                jaccard_denominator += max(vector_array1[idx][i][1], vector_array2[idx][j][1])
                i+=1
                j+=1
            elif (vector_array1[idx][i][0] < vector_array2[idx][j][0]):
                jaccard_denominator += vector_array1[idx][i][1]
                i+=1
            else:
                jaccard_denominator += vector_array2[idx][j][1]
                j+=1
        while (i < vector1_size):
            jaccard_denominator += vector_array1[idx][i][1]
            i += 1
        while (j < vector2_size):
            jaccard_denominator += vector_array2[idx][j][1]
            j += 1
        sim_array.append(jaccard_numerator / jaccard_denominator)


    for idx, val in enumerate(vector_array1):
        dice_numerator = 0
        dice_denominator = 0
        i = 0
        j = 0
        while (i < vector1_size and j < vector2_size):
            if (vector_array1[idx][i][0] == vector_array2[idx][j][0]):
                dice_numerator += min(vector_array1[idx][i][1], vector_array2[idx][j][1])
                dice_denominator += (vector_array1[idx][i][1] + vector_array2[idx][j][1])
                i+=1
                j+=1
            elif (vector_array1[idx][i][0] < vector_array2[idx][j][0]):
                dice_denominator += (vector_array1[idx][i][1])
                i+=1
            else:
                dice_denominator += (vector_array2[idx][j][1])
                j+=1
        while (i < vector1_size):
            dice_denominator += (vector_array1[idx][i][1])
            i += 1
        while (j < vector2_size):
            dice_denominator += (vector_array2[idx][j][1])
            j += 1
        sim_array.append((2 * dice_numerator) / dice_denominator)

    result = [word1 , word2 , flag.replace("\n","") , str(sim_array)]    
    sys.stdout.write("\t".join(result) + "\n")


if __name__ == '__main__':
    main()