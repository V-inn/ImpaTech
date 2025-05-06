def hanoi(peca, inicio, trabalho, final, quantDeJogadas):
    if peca == 1:
        print(str(quantDeJogadas+1) + " | Peça 1 | De: " + inicio + " Para: " + final)
        quantDeJogadas += 1
        return quantDeJogadas
    else:
        quantDeJogadas = hanoi(peca-1, inicio, final, trabalho, quantDeJogadas)
        print(str(quantDeJogadas+1) + " | Peça "+str(peca)+" | De: " + inicio + " Para: " + final)
        quantDeJogadas = hanoi(peca-1, trabalho, inicio, final, quantDeJogadas+1)

        return quantDeJogadas

pecas = input("Com quantas pecas quer jogar? ")
print("Total = ", hanoi(int(pecas), "A", "B", "C", 0))