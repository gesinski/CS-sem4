import time
import copy
import numpy as np
import math
import matplotlib.pyplot as plt

def create_matrix(a1, a2, a3, N):
    matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i == j:
                matrix[i][j] = a1
                if i < N-1 and j < N-1:
                    matrix[i+1][j] = a2
                    matrix[i][j+1] = a2
                if i < N-2 and j < N-2:
                    matrix[i+2][j] = a3
                    matrix[i][j+2] = a3
    return matrix
            
def create_vector(f, N):
    vector = np.zeros(N)
    n = 1
    for i in range(N):
        vector[i] = math.sin(n * (f + 1))
        n += 1
    return vector

def plot_residuum(residuum_data, method):
    plt.figure(figsize=(10, 6))
    plt.semilogy(residuum_data, label=method, color='blue')
    
    plt.xlabel('Iteracja')
    plt.ylabel('Norma residuum')
    plt.title(f'{method}')
    plt.legend()
    plt.grid(True)
    plt.show()

def jacobi_solve(A, L, U, D, b, x, residuum_norm, plot=True):
    iterations = 0
    inorm = A @ x - b
    M = -np.linalg.solve(D, L + U)
    w = np.linalg.solve(D, b)
    residuums = []

    start_time = time.time()
    while np.linalg.norm(inorm) > residuum_norm and iterations < 10000:
        x = M @ x + w
        iterations += 1
        inorm = A @ x - b
        residuums.append(np.linalg.norm(inorm))

        if np.any(np.isnan(np.linalg.norm(inorm))) or np.any(np.isinf(np.linalg.norm(inorm))):
            print("NaN or Inf encountered in Jacobi")
            break
    
    elapsed_time = time.time() - start_time
    print("Iterations jacobi:", iterations)
    print(f"Elapsed time Jacobi: {elapsed_time:.4f} seconds")
    if plot is True:
        plot_residuum(residuums, 'Jacobi')
    print()
    
    return elapsed_time

def gauss_seidle_solve(A, L, U, D, b, x, residuum_norm, plot=True):
    iterations = 0
    inorm = A @ x - b
    T = -np.linalg.solve(D + L, U)
    w = np.linalg.solve(D + L, b)
    residuums = []

    start_time = time.time()
    while  np.linalg.norm(inorm) > residuum_norm and iterations < 10000:
        x = T @ x + w
        iterations += 1
        inorm = A @ x - b
        residuums.append(np.linalg.norm(inorm))

        if np.any(np.isnan(np.linalg.norm(inorm))) or np.any(np.isinf(np.linalg.norm(inorm))):
            print("NaN or Inf encountered in Gauss-Siedle")
            break

    elapsed_time = time.time() - start_time
    print("Iterations gauss_seidle:", iterations)
    print(f"Elapsed time Gauss-Seidle: {elapsed_time:.4f} seconds")
    if plot is True:
        plot_residuum(residuums, 'Gauss-Seidle')
    print()

    return elapsed_time

def iteration_methods(A, b, N, plot=True):
    residuum_norm = 10 ** -9
    x0 = np.ones(N)
    L = np.tril(A, k=-1)
    U = np.triu(A, k =1)
    D = np.diag(np.diag(A))
    
    jacobi_time = jacobi_solve(A, L, U, D, b, x0.copy(), residuum_norm, plot)
    gauss_seidle_time = gauss_seidle_solve(A, L, U, D, b, x0.copy(), residuum_norm, plot)

    return jacobi_time, gauss_seidle_time

def LU(A, N):
    U = copy.copy(A)
    L = np.eye(N)
    for i in range(2, N+1):
        for j in range(1, i):
            L[i-1, j-1] = U[i-1, j-1] / U[j-1, j-1]
            U[i-1, :] = U[i-1, :] - L[i-1, j-1] * U[j-1, :]
    return L, U

def direct_method(A, b, N):
    start_time = time.time()

    L, U = LU(A, N)

    y = np.linalg.solve(L, b)
    x = np.linalg.solve(U, y)

    elapsed_time = time.time() - start_time
    
    residuum_norm = np.linalg.norm(A @ x - b)
    print("Direct residuum norm", residuum_norm)
    print(f"Elapsed time direct: {elapsed_time:.4f} seconds")
    print()
    return elapsed_time

index = "197995"
N = 1200 + 10*int(index[-2]) + int(index[-1])

#ex. A 
a1 = 5 + int(index[3])
a2 = a3 = -1
A = create_matrix(a1, a2, a3, N)

f = int(index[2])
b = create_vector(f, N)

#ex. B
iteration_methods(A, b, N, True)

#ex. C
a1 = 3
A = create_matrix(a1, a2, a3, N)
iteration_methods(A, b, N, True)

#ex. D
direct_method(A, b, N)

#ex. E
N = [100, 500, 1000, 2000, 3000, 5000]
jacobi_times = []
gauss_seidle_times = []
direct_times = []

for i in range(len(N)):
    a1 = 5 + int(index[3])
    a2 = a3 = -1
    A = create_matrix(a1, a2, a3, N[i])
    b = create_vector(f, N[i])
    jacobi_time, gauss_seidle_time = iteration_methods(A, b, N[i], False)
    direct_time = direct_method(A, b, N[i])
    jacobi_times.append(jacobi_time)
    gauss_seidle_times.append(gauss_seidle_time)
    direct_times.append(direct_time)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

colors = {
    'Jacobi': 'blue',
    'Gauss-Seidel': 'green',
    'Direct Method': 'red'
}

ax1.plot(N, jacobi_times, color=colors['Jacobi'], label='Jacobi')
ax1.plot(N, gauss_seidle_times, color=colors['Gauss-Seidel'], label='Gauss-Seidel')
ax1.plot(N, direct_times, color=colors['Direct Method'], label='Direct Method')
ax1.set_xlabel('Liczba niewiadomych N')
ax1.set_ylabel('Czas wyznaczenia rozwiązania [s]')
ax1.legend()
ax1.grid(True)

ax2.plot(N, jacobi_times, color=colors['Jacobi'], label='Jacobi')
ax2.plot(N, gauss_seidle_times, color=colors['Gauss-Seidel'], label='Gauss-Seidel')
ax2.plot(N, direct_times, color=colors['Direct Method'], label='Direct Method')
ax2.set_xlabel('Liczba niewiadomych N')
ax2.set_ylabel('Czas wyznaczenia rozwiązania [s]')
ax2.set_yscale('log')
ax2.legend()
ax2.grid(True, which="both", ls="--")

plt.tight_layout()
plt.show()
