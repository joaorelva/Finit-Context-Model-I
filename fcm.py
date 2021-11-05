import math
import random
from datetime import datetime

def createContext(k,filename):

    index = 0
    table = {}
 
    textFile = open(filename, 'r')
    text = textFile.read()

    """
    arr = ""
    count = 0

    for char in text:
        if char not in arr:
            arr += char
            count += 1

    for c in arr:
        print(ord(c))
    """

    symbols = ['\n', ' ', '!', '"', '$', '%', "'", '(', ')', '*', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', '@', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    while not ((index+k) >= len(text)) :
        aux = ""
        i = 0
        while i<k:
            aux += text[index]
            index += 1
            i += 1
        if aux not in table.keys():
            table.update({aux:{text[index]:1}})
        else:
            if text[index] in table[aux].keys():
                table[aux][text[index]] += 1
            else:
                table[aux].update({text[index]:1})
        index -= k-1

    for key in table.keys():
        for sindex in symbols:
            if sindex not in table[key].keys():
                table[key].update({sindex:0})

    return table

        

"""
    while not ((index+k) >= len(text)) :
        i = 0
        aux = ""
        while i < k:
            aux += text[index]
            index += 1
            i += 1
        if aux not in table.keys():
            table.update({aux:{text[index]:1}})
        else:
            if text[index] in table[aux].keys():
                table[aux][text[index]] += 1
            else:
                table[aux].update({text[index]:1})

    for key in table.keys():
        for sindex in symbols:
            if sindex not in table[key].keys():
                table[key].update({sindex:0})
    """

    #return table

def calculateProbabilities(table,alpha):
    prob_table = {}
    sum_total = 0

    for i in table.keys():
        sum = 0
        for j in table[i].keys():
            sum += table[i][j]
        for k in table[i].keys():
            prob = 0
            prob = (table[i][k] + alpha) / (sum + (54*alpha))
            if i not in prob_table:
                prob_table.update({i:{k:prob}})
            else:
                prob_table[i].update({k:prob})
        sum_total += sum

    return prob_table,sum_total

def calculateEntropy(table,prob_table,sum_total):
    model_entropy = 0
    for i in prob_table.keys():
        submodel_entropy = 0
        sum = 0
        for j in prob_table[i].keys():
            prob = prob_table[i][j]
            submodel_entropy += - prob * math.log2(prob)
            sum += table[i][j]
        context_prob = sum / sum_total
        model_entropy += submodel_entropy * context_prob 
    return model_entropy

#######################MAIN############################
start = datetime.now()

k = 2
alpha = 1
table = createContext(k,'example.txt')
#print(table)
prob_table,sum_total = calculateProbabilities(table,alpha)
entropy = calculateEntropy(table,prob_table,sum_total)

print("For k = " + str(k) + " and alpha = " + str(alpha))
print("Entropy of the model: " + str(entropy))
print('Execution Time: ' + str(datetime.now() - start))

# k = 3 | 0.1 -> 2.6
# k = 2 | 1   -> 2
# k = 4 | 0.1 -> 1.9

#EXPECTED
#k=2   a=1      H=2.5352
#k=3   a=1/10   H=1.9699
#k=4   a=1/10   H=1.6893