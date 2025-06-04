fileName = input("Digite o nome do arquivo: ")

caminhoDoArquivo = "./Arquivos/"
try:
    arquivo = open(caminhoDoArquivo+fileName, "r+", encoding="utf-8")
except FileNotFoundError:
    print("Arquivo não encontrado")
    exit()

sair = ""
while(sair != "sair"):

    operacao = input("Digite 'r' para ler o arquivo ou 'w' para escrever nele: ")
    if operacao == "r":
        for linhas in arquivo:
            print(linhas.strip())
    elif operacao == "w":
        print("------------------------------------------------------")
        print("Você agora está digitando.\nDigite '\sair' para encerrar a escrita no arquivo.")
        print("------------------------------------------------------")
        entrada = ""
        arquivo.write("\n")  # Limpa o conteúdo do arquivo
        while entrada != "\sair":
            entrada = input()
            if entrada != "\sair":
                arquivo.write(entrada + "\n")
        print("-------------------------------------------------------")
    sair = input("Digite 'sair' para encerrar ou qualquer outra tecla para continuar: ")

arquivo.close()
