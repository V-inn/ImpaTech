def sort5elements(values):
    a = values[0]
    b = values[1]
    c = values[2]
    d = values[3]
    e = values[4]

    if a <= b:          #Primeira
        b,a = a,b
    if c <= d:          #Segunda
        d,c = c,d

    if a <= c:          #Terceira
        a,c,d,b = c,a,b,d

    if e <= c:          #Quarta
        if e >= d:      #Quinta
            c,d,e = c,e,d
    else:
        if e >= a:      #Quinta
            a,c,d,e = e,a,c,d
        else:
            c,d,e = e,c,d

    if b <= d:          #Sexta
        if b <= e:      #Setima
            b,c,d,e = c,d,e,b
        else:
            b,c,d = c,d,b
    else:
        if b <= c:      #Setima
            b,c = c,b

    return [e, d, c, b, a]

if __name__ == '__main__':
    print(sort5elements([5,4,3,2,1]))
    print(sort5elements([351,2,125,25,2]))
    print(sort5elements([0,1,6,5,1]))

    valor = list(map(int, input().split()))
    print(sort5elements(valor))

# Por Vinícius Flesch Kern