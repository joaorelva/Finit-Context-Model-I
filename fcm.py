import math
import random
from datetime import datetime

def createContext(k,filename):

    index = 0
    table = {}
 
    textFile = open(filename, 'r')
    text = textFile.read()

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

k = 3
alpha = 0.1
table = createContext(k,'example.txt')
prob_table,sum_total = calculateProbabilities(table,alpha)
entropy = calculateEntropy(table,prob_table,sum_total)
print("--------------------------------------------------------------")
print("-------------------------FCM RESULTS--------------------------")
print("--------------------------------------------------------------")
print("For k = " + str(k) + " and alpha = " + str(alpha))
print("Entropy of the model: " + str(entropy))
#######################GENERATOR############################
text = "thi"
state = 'thi'
length = 700


while len(text) != length:
    if state not in prob_table.keys():
        text += " "
        aux = random.choices(list(prob_table.keys()))
        c = ' '.join(aux)
        state = c
    i = 0
    index = 0
    new_state = ""
    #print("state : " + str(state))
    letter = random.choices(population=list(prob_table[state].keys()), weights=prob_table[state].values())
    car = ' '.join(letter)
    text += car
    #print("text : " + str(text))
    while i < k-1:
        new_state += state[index+1]
        i += 1
        index += 1
    new_state += car
    #print("newstate : " + str(new_state))
    state = new_state

print("--------------------------------------------------------------")
print("------------------------TEXT GENERATED------------------------")
print("--------------------------------------------------------------")

print(text)

print("--------------------------------------------------------------")
print("------------------------EXECUTION TIME------------------------")
print("--------------------------------------------------------------")
print(str(datetime.now() - start))






# k = 3 | 0.1 -> 2.6
# k = 2 | 1   -> 2
# k = 4 | 0.1 -> 1.9

#EXPECTED
#k=2   a=1      H=2.5352
#k=3   a=1/10   H=1.9699
#k=4   a=1/10   H=1.6893