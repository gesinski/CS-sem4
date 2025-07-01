import random

def odwr_dystrybuanta(N):
    liczby = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for _ in range(N):
        losowa = random.random() * 100 + 50
        liczby[int((losowa - 50) * 0.1 )] += 1
    return liczby

N = 100000

print("zad1: ", odwr_dystrybuanta(N))

def odwr_dystrybuanta2(N, X, p):
    ilosc_wystapien = [0, 0, 0, 0]
    for _ in range(N):
        suma = 0.0
        losowa = random.random()
        i = 0
        while losowa >= suma:
            suma += p[i]
            i += 1
        ilosc_wystapien[X[i-1]-1] += 1  
    return ilosc_wystapien  
    

X = [1, 2, 3, 4]
p = [0.1, 0.4, 0.2, 0.3]

print("zad2: ", odwr_dystrybuanta2(N, X, p))
