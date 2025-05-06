#Por Vinicius Flesch Kern


#Não mudar
bolinha = -1
xis = 1

terminar = False

tabela = [[0,0,0],
          [0,0,0],
          [0,0,0]]

def encerrarJogoAbruptamente():
    print("\n Jogo encerrado pelo console.")
    terminar = True
    terminarRodada = True

def imprimirTabela():
    print("")
    print("0 1 2")
    for indice_linha, linha in enumerate(tabela):
        for elemento in linha:
            if elemento == xis:
                print("X", end=" ")
            elif elemento == bolinha:
                print("O", end=" ")
            else:
                print("-", end=" ")    
        print(str(indice_linha) + " ")
    print("")

#imprimir()

def verificarJogada(jogada):
    lin = jogada[0]
    col = jogada[1]

    if len(jogada) != 2:
        print("Por favor digite somente dois valores.")
        return False
    
    if(lin.isnumeric() and col.isnumeric()):
        lin = int(lin)
        col = int(col)
    else:
        print("Por favor digite somente numeros.")
        return False

    if (lin < 0 or lin > 2) or (col < 0 or col > 2):
        print("Por favor digite numeros validos para linhas e colunas.")
        return False

    if(tabela[lin][col] == 0):
        return True
    else:
        print("Essa casa já esta ocupada.")
        return False

def verificarVitoria():
    somaDiagonalUm = 0
    somaDiagonalDois = 0

    for i in range(0, len(tabela)):
        somaLinhaAtual = 0
        somaColunaAtual = 0
        
        somaDiagonalUm = somaDiagonalUm + tabela[i][i]
        somaDiagonalDois = somaDiagonalDois + tabela[2-i][i]

        for j in range(0, len(tabela)):
            somaLinhaAtual = somaLinhaAtual + tabela[i][j]
            somaColunaAtual = somaColunaAtual + tabela[j][i]

        """print("Soma coluna "+ str(i) + ": " + str(somaColunaAtual))
        print("Soma linha " + str(i) + ": " + str(somaLinhaAtual))
        print("")"""

        if somaLinhaAtual == 3 or somaColunaAtual == 3:
            return 1
        elif somaLinhaAtual == -3 or somaColunaAtual == -3:
            return -1
        
    """print("Soma diagonal 1:", somaDiagonalUm)
    print("Soma diagonal 2:", somaDiagonalDois)
    print("---------------")"""
    
    if somaDiagonalUm == 3 or somaDiagonalDois == 3:
        return 1
    elif somaDiagonalUm == -3 or somaDiagonalDois == -3:
        return -1
    else:
        return 0

while not terminar:
    jogadaAtual = 0
    terminarRodada = False

    tabela = [[0,0,0],
            [0,0,0],
            [0,0,0]]

    while not terminarRodada:
        imprimirTabela()

        vitoria = verificarVitoria()

        if(vitoria == 0):
            try:
                jogada = input("Digite sua jogada na forma 'LINHA COLUNA': ")

                jogada = jogada.split()

                if(verificarJogada(jogada)):
                    lin = int(jogada[0])
                    col = int(jogada[1])
                    jogador = 0

                    if(jogadaAtual%2 == 0):
                        jogador = xis
                    else:
                        jogador = bolinha
                    

                    tabela[lin][col] = jogador

                    jogadaAtual += 1

                    if jogadaAtual == 9:
                        print("Empate.")
                        terminarRodada = True
                        imprimirTabela()

            except KeyboardInterrupt:
                encerrarJogoAbruptamente()
                
        elif vitoria == -1:
            print("O venceu.")
            terminarRodada = True
        elif vitoria == 1:
            print("X venceu.")
            terminarRodada = True
            

    while not terminar:
        reiniciar = "N"

        try:
            reiniciar = input("Deseja recomeçar? S/N: ")
        except KeyboardInterrupt:
            reiniciar == "N"

        if reiniciar == "N":
            print("Jogo encerrado")
            terminar = True
        elif reiniciar == "S":
            break
        else:
            print("Entrada desconhecida.")
            print("---------------------")