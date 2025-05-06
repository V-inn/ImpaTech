def busca_binaria(v, n, a, b):
    if(b>=a):
        meio = (a+b)//2
        elMeio = v[meio]
        if n == elMeio:
            return meio
        elif(n>elMeio):
            return busca_binaria(v, n, meio+1, b)
        else:
            return busca_binaria(v, n, a, meio-1)
    else:
        return -1

a = [1,2,8,9,12,56,57,100,101,206,275,300,1400]
buscar = float(input("Insira o valor a ser buscado: "))
print(busca_binaria(a, buscar, 0, len(a)-1))