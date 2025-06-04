entrada = list(map(int, input().split()))
pontoPorRodada = list(map(int, input().split()))

jogadores = entrada[0]
rodadas = entrada[1]

pontuacao = []

for i in range(0, jogadores):
    pontuacao.append(0)
    for j in range(0, rodadas):
        pontuacao[i]+=pontoPorRodada[i+j*jogadores]

vencedor = 0
maiorPontuacao = 0
for i in range(0, len(pontuacao)):
    if pontuacao[i] >= maiorPontuacao:
        maiorPontuacao = pontuacao[i]
        vencedor = i+1
        
print(vencedor)