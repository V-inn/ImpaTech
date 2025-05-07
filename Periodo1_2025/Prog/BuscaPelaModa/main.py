a = [10,19,14,5,7,6,19,7,8,10,7,7,19,19,12,12,12,12]
b = []
c = [1,2,3,4,5]
d = [1,1,1,1,1,1]

def BuscarModa(lista):
    lineDivision = "---------------------"

    if(len(lista)==0):
        print("Lista vazia")
        print(lineDivision)
        return

    modas = [[0,0]] #Primeiro valor é uma 'chave' e segundo valor a quantidade de vezes que aparece
    maiorElemento = [0]

    def adicionar(elemento):
        elemento = str(elemento)
        for el in modas:
            if(elemento == el[0]):
                el[1]+=1
                return
        modas.append([elemento, 1])
        
    for elemento in lista:
        adicionar(elemento)
    
    """
        1) Verifica se o elemento i da lista apareceu a mesma quantidade que o 
        primeiro dos elementos que mais apareceram antes
        
        2) Verifica se o elemento i da lista apareceu mais que o primeiro dos 
        elementos que apareceram antes
    """
    for i in range(0, len(modas)):
        if modas[i][1] == modas[maiorElemento[0]][1]: #(1)
            maiorElemento.append(i)
        elif modas[i][1] > modas[maiorElemento[0]][1]: #(2)
            maiorElemento = [i]

    for elemento in maiorElemento:
        print(str(modas[elemento][0]) + " aparece " + str(modas[elemento][1]) + " vez(es)")

    print(lineDivision)


BuscarModa(a)
BuscarModa(b)
BuscarModa(c)
BuscarModa(d)
