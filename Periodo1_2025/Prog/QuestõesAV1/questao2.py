contagem = 0
while(True):
    contagem+=1
    quantPessoas = int(input())
    if quantPessoas == 0:
        break

    chegada = list(map(int, input().split()))

    ganhador = 0
    for i in range(0, quantPessoas):
        if chegada[i] == i+1:
            ganhador = chegada[i]
            break

    print("Teste", contagem)
    print(ganhador)
    print()