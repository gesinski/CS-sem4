def gorszy_random(n):
    a = 69069
    c = 1
    X = 15
    M = 2 ** 31
    numbers = []
    for i in range(n):
        X = (a * X + c) % M
        numbers.append(X)
    return numbers

M = 2 ** 31
n = 100000
view = []
view = gorszy_random(n)

count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in range(n):
    count[int(view[i] / (M * 0.1))] += 1
print(count)


def gorszy_random2(n):
    p = 7
    q = 3
    numbers = []
    b = [1, 0, 1, 1, 0, 1, 1]

    for j in range(7, 31):
        b.append(b[j - p] ^ b[j - q])

    numbers.append(b[:])

    for i in range(1, n):
        b2 = numbers[i - 1]
        b = b2[24:31]

        for j in range(7, 31):
            b.append(b[j - p] ^ b[j - q])

        numbers.append(b[:])

    return numbers


def list_to_int(b_list):
    b = 0
    a = 2
    for i in range(len(b_list)):
        if i != 31:
            b += b_list[i] * (a ** i)
        else:
            b += b_list[i] * ((a ** i-1))
    return b

view2 = gorszy_random2(n)

count2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

M = (2 ** 31)

for i in range(n):
    index = int(list_to_int(view2[i]) / (M * 0.1))
    if 0 <= index < len(count2):
        count2[index] += 1
print(count2)