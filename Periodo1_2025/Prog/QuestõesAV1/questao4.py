quantTestes = int(input())
testeAtual = 0

entradas = []

def executarMovimento(pos, posAtual):
        if entradas[pos] == "L":
            posAtual -= 1
        elif entradas[pos] == "R":
            posAtual += 1
        else:
            posAtual = executarMovimento(int(entradas[pos])-1, posAtual)
        return posAtual

while(testeAtual < quantTestes):
    testeAtual+=1
    posicaoAtual = 0
    quantEntradas = int(input())

    entradas = []

    for i in range(0, quantEntradas):
        entrada = input()
        if entrada == "LEFT":
            entrada = "L"
        elif entrada == "RIGHT":
            entrada = "R"
        else:
            entrada = entrada.split()[2]
        entradas.append(entrada)

    for i in range(0, quantEntradas):
        posicaoAtual = executarMovimento(i,posicaoAtual)

    print(posicaoAtual)
            
