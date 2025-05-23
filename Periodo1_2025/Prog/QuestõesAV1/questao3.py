quantTestes = int(input())

testes = []

#Armazena todos as entradas antes de executar
for i in range(0, quantTestes):
    testeAtual = input()
    testes.append(testeAtual)

for i in range(0, quantTestes):
    entrada = testes[i].split()
    resultado = ""
    if(len(entrada) != 0):
        for j in range(0, len(entrada)):
            resultado += entrada[j][0]
    print(resultado)