from datetime import datetime
import random
import sys
from fcm import createContext,calculateProbabilities,calculateEntropy

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("The program should be called like this: \n\tpython3 generator.py filename k alpha textlength firststate")
    else:
        filename = sys.argv[1]
        k = int(sys.argv[2])
        alpha = float(sys.argv[3])
        length = int(sys.argv[4])
        state = sys.argv[5]

        start = datetime.now()

        table = createContext(k,filename)
        prob_table,sum_total = calculateProbabilities(table,alpha)
        entropy = calculateEntropy(table,prob_table,sum_total)

        print("--------------------------------------------------------------")
        print("-------------------------FCM RESULTS--------------------------")
        print("--------------------------------------------------------------")
        print("For k = " + str(k) + " and alpha = " + str(alpha))
        print("Entropy of the model: " + str(entropy))

        text = state

        while len(text) != length:
            if state not in prob_table.keys():
                #ISTO TEM DE SER MUDADO!! O QUE ESTA A FAZER E QUE QUANDO O CONTEXTO USADO PARA PREVER A PROXIMA LETRA
                #NAO EXISTE NA TABELA, É ACRESCENTADO UM ESPAÇO AO TEXTO E ESCOLHIDO UM CONTEXTO DA TABELA ALEATORIO
                text += " "
                aux = random.choices(list(prob_table.keys()))
                c = ' '.join(aux)
                state = c
            i = 0
            index = 0
            new_state = ""
            letter = random.choices(population=list(prob_table[state].keys()), weights=prob_table[state].values())
            car = ' '.join(letter)
            text += car
            while i < k-1:
                new_state += state[index+1]
                i += 1
                index += 1
            new_state += car
            state = new_state

        print("--------------------------------------------------------------")
        print("------------------------TEXT GENERATED------------------------")
        print("--------------------------------------------------------------")

        print(text)

        print("--------------------------------------------------------------")
        print("------------------------EXECUTION TIME------------------------")
        print("--------------------------------------------------------------")
        print(str(datetime.now() - start))