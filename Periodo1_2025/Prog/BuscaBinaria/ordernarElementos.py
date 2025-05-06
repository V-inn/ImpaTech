def minimum(v,ini):
    menor_elemento = ini
    for i in range(ini+1, len(v)):
        if v[i]<v[menor_elemento]:
            menor_elemento = i

    return menor_elemento

def ordenar(v, i):
    if i == (len(v)-1):
        return v
    else:
        indice_min = minimum(v,i)
        v[indice_min],v[i]=v[i],v[indice_min]
        i+=1
        return ordenar(v,i)
    
def ordenarIterativa(v,i):
    for i in range(0, len(v)):
        indice_min = minimum(v,i)
        v[indice_min],v[i]=v[i],v[indice_min]
    return v

v=[6,35,7,23,89,3,1,7,0,-1,-9,0,-15,10000,-1000]
#print(ordenar(v,0))
print(ordenarIterativa(v,0))
