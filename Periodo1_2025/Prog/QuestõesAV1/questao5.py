quantEntradas = int(input())

listaPares = []
listaImpares = []

for i in range(0, quantEntradas):
    valor = int(input())
    if valor % 2 == 0:
        listaPares.append(valor)
    else:
        listaImpares.append(valor)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j],arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i+1

def quickSort(arr, low, high):
    if low < high:
        
        pi = partition(arr, low, high)
        
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)

lenPares = len(listaPares)
lenImpares = len(listaImpares)
quickSort(listaPares,0,lenPares-1)
quickSort(listaImpares,0,lenImpares-1)

for i in range(0, lenPares):
    print(listaPares[i])

for i in range(0, lenImpares):
    print(listaImpares[lenImpares-i-1])