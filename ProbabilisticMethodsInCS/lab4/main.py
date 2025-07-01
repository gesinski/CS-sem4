import random

def get_x_place(px):
    sum = 0.0
    rand_num = random.random()
    i = 0
    while rand_num >= sum:
        sum += px[i]
        i += 1
    return i

def get_y_place(rand_y, prob):
    sum = 0.0
    i = 0
    while rand_y >= sum:
        sum += prob[i]
        i += 1
    return i

def get_py(prob, x):
    py = [0, 0, 0, 0]
    sum = 0
    for i in range(len(prob[0])):
        sum += prob[x-1][i]
    for i in range(len(prob[0])):
        py[i] = prob[x-1][i] / sum
    return py

def f(X, Y, Prob, N):
    occurance = [[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
    px = []
    for i in range(len(X)):
        sum = 0
        for j in range(len(Y)):
            sum += Prob[i][j]
        px.append(sum)
    for _ in range(N):
        x = get_x_place(px)
        rand_y = random.random()
        if x == 1:
            py = get_py(Prob, x)
            y = get_y_place(rand_y, py)
        elif x == 2:
            py = get_py(Prob, x)
            y = get_y_place(rand_y, py)
        elif x == 3:
            py = get_py(Prob, x)
            y = get_y_place(rand_y, py)
        elif x == 4:
            py = get_py(Prob, x)
            y = get_y_place(rand_y, py)
        occurance[x-1][y-1] += 1  
    return occurance

X = [1, 2, 3, 4]
Y = [1, 2, 3, 4]
Prob = [[0, 0, 0.17, 0],
     [0.1, 0, 0, 0],
     [0, 0, 0.2, 0.3],
     [0.03, 0.2, 0, 0]]
N = 100000

print(f(X, Y, Prob, N))
