files=['results100/part-00000','results100/part-00001','results100/part-00002','results100/part-00003','results100/part-00004','results100/part-00005'
    ,'results100/part-00006','results100/part-00007']


with open ("datawithwords.arff","a+") as output:
    output.write("@RELATION similar\n")
    output.write("@ATTRIBUTE 'wordPair'	string\n")
    output.write("@ATTRIBUTE 'related'	{True, False}\n")
    output.write("@ATTRIBUTE 'man1'	real\n")
    output.write("@ATTRIBUTE 'man2'	real\n")
    output.write("@ATTRIBUTE 'man3'	real\n")
    output.write("@ATTRIBUTE 'man4'	real\n")
    output.write("@ATTRIBUTE 'euc1'	real\n")
    output.write("@ATTRIBUTE 'euc2'	real\n")
    output.write("@ATTRIBUTE 'euc3'	real\n")
    output.write("@ATTRIBUTE 'euc4'	real\n")
    output.write("@ATTRIBUTE 'cos1'	real\n")
    output.write("@ATTRIBUTE 'cos2'	real\n")
    output.write("@ATTRIBUTE 'cos3'	real\n")
    output.write("@ATTRIBUTE 'cos4'	real\n")
    output.write("@ATTRIBUTE 'jac1'	real\n")
    output.write("@ATTRIBUTE 'jac2'	real\n")
    output.write("@ATTRIBUTE 'jac3'	real\n")
    output.write("@ATTRIBUTE 'jac4'	real\n")
    output.write("@ATTRIBUTE 'dic1'	real\n")
    output.write("@ATTRIBUTE 'dic2'	real\n")
    output.write("@ATTRIBUTE 'dic3'	real\n")
    output.write("@ATTRIBUTE 'dic4'	real\n")
    output.write("@DATA\n")
    for name in files:
        with open (name) as file:
            for line in file:
                word1, word2, flag, vector = line.split('\t')
                words= word1 + "-" + word2
                result =words + "," + flag + "," + vector
                result = result.replace('\t', ',')
                result = result.replace('[', '')
                result = result.replace(']', '')
                result = result.replace(' ', '')
                output.write(result)