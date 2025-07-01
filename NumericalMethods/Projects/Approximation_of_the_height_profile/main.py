import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_nodes(data, nodes_num):
    indices = np.linspace(0, len(data) - 1, num=nodes_num, dtype=int)
    selected_nodes = data.iloc[indices].reset_index(drop=True)

    return selected_nodes

def scale_field(data):
    min_val = data['Dystans (m)'].min()
    max_val = data['Dystans (m)'].max()
    
    data_scaled = (data['Dystans (m)'] - min_val) / (max_val - min_val)
    data['Dystans (m)'] = data_scaled
    return data

def unscale_field(data, data_scaled):
    x_min = data['Dystans (m)'].min()
    x_max = data['Dystans (m)'].max()

    data_scaled['Dystans (m)'] = data_scaled['Dystans (m)'] * (x_max - x_min) + x_min

    return data_scaled

def lagrange_interpolation(data, num_points=1000):
    x = data['Dystans (m)'].values
    y = data['Wysokość (m)'].values

    def L(k, x_val):
        terms = [(x_val - x[j]) / (x[k] - x[j]) for j in range(len(x)) if j != k]
        return np.prod(terms)

    x_new = np.linspace(x.min(), x.max(), num_points)
    y_new = []

    for x_val in x_new:
        interpolated = sum(y[k] * L(k, x_val) for k in range(len(x)))
        y_new.append(interpolated)

    result = pd.DataFrame({
        'Dystans (m)': x_new,
        'Wysokość (m)': y_new
    })

    return result

def spline_interpolation(data, num_points=1000):
    x = data['Dystans (m)'].values
    y = data['Wysokość (m)'].values
    n = len(x)

    h = np.diff(x)

    alpha = np.zeros(n)
    for i in range(1, n - 1):
        alpha[i] = (3/h[i]) * (y[i+1] - y[i]) - (3/h[i-1]) * (y[i] - y[i-1])

    l = np.ones(n)
    mu = np.zeros(n)
    z = np.zeros(n)

    for i in range(1, n - 1):
        l[i] = 2 * (x[i+1] - x[i-1]) - h[i-1] * mu[i-1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i-1]*z[i-1]) / l[i]

    c = np.zeros(n)
    b = np.zeros(n-1)
    d = np.zeros(n-1)
    a = y[:-1]

    for j in reversed(range(n - 1)):
        c[j] = z[j] - mu[j] * c[j+1]
        b[j] = (y[j+1] - y[j])/h[j] - h[j]*(c[j+1] + 2*c[j])/3
        d[j] = (c[j+1] - c[j]) / (3*h[j])

    x_new = np.linspace(x[0], x[-1], num_points)
    y_new = np.zeros_like(x_new)

    for i in range(len(x_new)):
        for j in range(n - 1):
            if x[j] <= x_new[i] <= x[j+1]:
                dx = x_new[i] - x[j]
                y_new[i] = a[j] + b[j]*dx + c[j]*dx**2 + d[j]*dx**3
                break

    return pd.DataFrame({'Dystans (m)': x_new, 'Wysokość (m)': y_new})

def plot_multiple_lagrange_interpolations(data, num_nodes_list, num_points=1000):
    custom_colors = [
        '#e41a1c',  # czerwony
        '#377eb8',  # niebieski
        '#4daf4a',  # zielony
        '#984ea3',  # fioletowy
        '#ff7f00',  # pomarańczowy
        '#ffff33',  # żółty
        '#a65628',  # brązowy
        '#f781bf',  # różowy
        '#999999',  # szary
        '#66c2a5'   # morski
    ]

    plt.figure(figsize=(12, 7))

    plt.plot(data['Dystans (m)'], data['Wysokość (m)'], '-', color='black', label='Oryginalne dane', linewidth=1.5)

    for idx, nodes_num in enumerate(num_nodes_list):
        color = custom_colors[idx % len(custom_colors)]

        nodes = get_nodes(data, nodes_num)
        nodes_scaled = scale_field(nodes.copy())

        interp = lagrange_interpolation(nodes_scaled, num_points)
        interp = unscale_field(data, interp)

        nodes_unscaled = unscale_field(data, nodes_scaled.copy())

        plt.plot(interp['Dystans (m)'], interp['Wysokość (m)'],
                 '-', label=f'Liczba węzłów: {nodes_num}', color=color, linewidth=2)

        plt.plot(nodes_unscaled['Dystans (m)'], nodes_unscaled['Wysokość (m)'],
                 'o', markerfacecolor='none', markeredgecolor=color, markersize=7, markeredgewidth=1.5,
                 label=f'Węzły {nodes_num}')

    #plt.title("Interpolacja Lagrange'a dla różnej liczby węzłów", fontsize=14)
    plt.xlabel("Dystans (m)")
    plt.ylabel("Wysokość (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_multiple_spline_interpolations(data, num_nodes_list, num_points=1000):
    custom_colors = [
        '#e41a1c', '#377eb8', '#4daf4a',
        '#984ea3', '#ff7f00', '#ffff33',
        '#a65628', '#f781bf', '#999999', '#66c2a5'
    ]

    plt.figure(figsize=(12, 7))

    plt.plot(data['Dystans (m)'], data['Wysokość (m)'],
             '-', color='black', label='Oryginalne dane', linewidth=1.5)

    for idx, nodes_num in enumerate(num_nodes_list):
        color = custom_colors[idx % len(custom_colors)]

        nodes = get_nodes(data, nodes_num)
        nodes_scaled = scale_field(nodes.copy())

        interp = spline_interpolation(nodes_scaled, num_points)
        interp = unscale_field(data, interp)

        nodes_unscaled = unscale_field(data, nodes_scaled.copy())

        plt.plot(interp['Dystans (m)'], interp['Wysokość (m)'],
                 '-', label=f'Liczba węzłów: {nodes_num}', color=color, linewidth=2)

        plt.plot(nodes_unscaled['Dystans (m)'], nodes_unscaled['Wysokość (m)'],
                 'o', markerfacecolor='none', markeredgecolor=color, markersize=7, markeredgewidth=1.5,
                 label=f'Węzły {nodes_num}')

    plt.xlabel("Dystans (m)")
    plt.ylabel("Wysokość (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_interpolation_errors(data, num_nodes_list, num_points=1000):
    x_dense = np.linspace(data['Dystans (m)'].min(), data['Dystans (m)'].max(), num_points)
    y_dense = np.interp(x_dense, data['Dystans (m)'], data['Wysokość (m)'])  # oryginalna funkcja (aproksymacja)

    custom_colors = [
        '#e41a1c', '#377eb8', '#4daf4a',
        '#984ea3', '#ff7f00', '#ffff33'
    ]

    plt.figure(figsize=(12, 6))

    for idx, nodes_num in enumerate(num_nodes_list):
        color = custom_colors[idx % len(custom_colors)]

        nodes = get_nodes(data, nodes_num)
        nodes_scaled = scale_field(nodes.copy())

        interp = lagrange_interpolation(nodes_scaled, num_points)
        interp = unscale_field(data, interp)

        y_interp_aligned = np.interp(x_dense, interp['Dystans (m)'], interp['Wysokość (m)'])

        error = np.abs(y_dense - y_interp_aligned)

        plt.plot(x_dense, error, label=f'Liczba węzłów: {nodes_num}', color=color)

    #plt.title("Porównanie błędów interpolacji względem danych oryginalnych", fontsize=14)
    plt.xlabel("Dystans (m)")
    plt.ylabel("Błąd bezwzględny |f_oryg(x) - f_interpol(x)|")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_spline_interpolation_errors(data, num_nodes_list, num_points=1000):
    x_dense = np.linspace(data['Dystans (m)'].min(), data['Dystans (m)'].max(), num_points)
    y_dense = np.interp(x_dense, data['Dystans (m)'], data['Wysokość (m)'])  # oryginalna aproksymacja

    custom_colors = [
        '#e41a1c', '#377eb8', '#4daf4a',
        '#984ea3', '#ff7f00', '#ffff33',
        '#a65628', '#f781bf', '#999999', '#66c2a5'
    ]

    plt.figure(figsize=(12, 6))

    for idx, nodes_num in enumerate(num_nodes_list):
        color = custom_colors[idx % len(custom_colors)]

        nodes = get_nodes(data, nodes_num)
        nodes_scaled = scale_field(nodes.copy())

        interp = spline_interpolation(nodes_scaled, num_points)
        interp = unscale_field(data, interp)

        y_interp_aligned = np.interp(x_dense, interp['Dystans (m)'], interp['Wysokość (m)'])

        error = np.abs(y_dense - y_interp_aligned)

        plt.plot(x_dense, error, label=f'Liczba węzłów: {nodes_num}', color=color)

    plt.xlabel("Dystans (m)")
    plt.ylabel("Błąd bezwzględny |f_oryg(x) - f_interpol(x)|")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_interpolation_error_sums(data, num_nodes_list, method='lagrange'):
    error_sums = []

    for num_nodes in num_nodes_list:
        nodes = get_nodes(data, num_nodes)
        nodes_scaled = scale_field(nodes.copy())

        if method == 'lagrange':
            interpolated = lagrange_interpolation(nodes_scaled, num_points=1000)
        elif method == 'spline':
            interpolated = spline_interpolation(nodes_scaled, num_points=1000)
        else:
            raise ValueError("Invalid method. Use 'lagrange' or 'spline'.")

        interpolated_unscaled = unscale_field(data, interpolated)

        x_interp = interpolated_unscaled['Dystans (m)'].values
        y_interp = interpolated_unscaled['Wysokość (m)'].values

        y_original_interp = np.interp(x_interp, data['Dystans (m)'], data['Wysokość (m)'])

        error = np.abs(y_original_interp - y_interp)
        total_error = np.sum(error)
        error_sums.append(total_error)

    plt.figure(figsize=(8, 6))
    plt.bar([str(n) for n in num_nodes_list], error_sums, color='teal')
    plt.xlabel("Liczba węzłów interpolacji")
    plt.ylabel("Suma błędów bezwzględnych")
    #plt.title(f"Porównanie sum błędów ({method.capitalize()} interpolation)")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def get_chebyshev_nodes(data, nodes_num):
    n = nodes_num
    x_cheb = np.array([
        0.5 * (1 + np.cos(np.pi * (2 * i + 1) / (2 * n))) for i in range(n)]) 
    x_cheb = x_cheb[::-1]  

    indices = (x_cheb * (len(data) - 1)).astype(int)
    selected_nodes = data.iloc[indices].reset_index(drop=True)
    return selected_nodes

def plot_lagrange_chebyshev_interpolations(data, num_nodes_list, num_points=1000):
    plt.figure(figsize=(12, 7))
    plt.plot(data['Dystans (m)'], data['Wysokość (m)'], '-', color='black', label='Oryginalne dane', linewidth=1.5)

    for idx, nodes_num in enumerate(num_nodes_list):
        color = f"C{idx}"

        nodes = get_chebyshev_nodes(data, nodes_num)
        nodes_scaled = scale_field(nodes.copy())

        interp = lagrange_interpolation(nodes_scaled, num_points)
        interp = unscale_field(data, interp)
        nodes_unscaled = unscale_field(data, nodes_scaled.copy())

        plt.plot(interp['Dystans (m)'], interp['Wysokość (m)'],
                 '-', label=f'Czebyszew {nodes_num} węzłów', color=color, linewidth=2)

        plt.plot(nodes_unscaled['Dystans (m)'], nodes_unscaled['Wysokość (m)'],
                 'o', markerfacecolor='none', markeredgecolor=color, markersize=7, markeredgewidth=1.5)

    plt.xlabel("Dystans (m)")
    plt.ylabel("Wysokość (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_spline_chebyshev_interpolations(data, num_nodes_list, num_points=1000):
    plt.figure(figsize=(12, 7))
    plt.plot(data['Dystans (m)'], data['Wysokość (m)'], '-', color='black', label='Oryginalne dane', linewidth=1.5)

    for idx, nodes_num in enumerate(num_nodes_list):
        color = f"C{idx}"

        nodes = get_chebyshev_nodes(data, nodes_num)
        nodes_scaled = scale_field(nodes.copy())

        interp = spline_interpolation(nodes_scaled, num_points)
        interp = unscale_field(data, interp)
        nodes_unscaled = unscale_field(data, nodes_scaled.copy())

        plt.plot(interp['Dystans (m)'], interp['Wysokość (m)'],
                 '-', label=f'Czebyszew {nodes_num} węzłów', color=color, linewidth=2)

        plt.plot(nodes_unscaled['Dystans (m)'], nodes_unscaled['Wysokość (m)'],
                 'o', markerfacecolor='none', markeredgecolor=color, markersize=7, markeredgewidth=1.5)

    plt.xlabel("Dystans (m)")
    plt.ylabel("Wysokość (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


mount_everest_data = pd.read_csv('MountEverest.csv')
bike_ride_data = pd.read_csv('Unsyncable_ride.csv')

#Lagrange

#Mount Everest

plot_multiple_lagrange_interpolations(mount_everest_data, [4, 6, 8])
plot_multiple_lagrange_interpolations(mount_everest_data, [10, 12, 14])

num_nodes = [7, 8, 9]
plot_multiple_lagrange_interpolations(mount_everest_data, num_nodes)

plot_interpolation_errors(mount_everest_data, num_nodes)
plot_interpolation_error_sums(mount_everest_data, num_nodes, method='lagrange')

#Bike Ride

plot_multiple_lagrange_interpolations(bike_ride_data, [4, 6, 8])
plot_multiple_lagrange_interpolations(bike_ride_data, [10, 12, 14])
num_nodes = [7, 8, 9]
plot_multiple_lagrange_interpolations(bike_ride_data, num_nodes)
plot_interpolation_errors(bike_ride_data, num_nodes)
plot_interpolation_error_sums(bike_ride_data, num_nodes, method='lagrange')


#Spline

#Mount Everest
plot_multiple_spline_interpolations(mount_everest_data, [4, 6, 8])
plot_multiple_spline_interpolations(mount_everest_data, [8, 10, 12])
plot_multiple_spline_interpolations(mount_everest_data, [12, 14, 16])
plot_multiple_spline_interpolations(mount_everest_data, [50, 100, 150])
plot_spline_interpolation_errors(mount_everest_data, [8, 12, 16])
plot_interpolation_error_sums(mount_everest_data, [8, 12, 16], method='spline')

#Bike Ride
plot_multiple_spline_interpolations(bike_ride_data, [4, 6, 8])
plot_multiple_spline_interpolations(bike_ride_data, [10, 12, 14])
plot_multiple_spline_interpolations(bike_ride_data, [15, 16, 17])
plot_interpolation_error_sums(bike_ride_data, [12, 14, 16], method='spline')
plot_multiple_spline_interpolations(bike_ride_data, [12, 14, 16])


#Chebyshev nodes
num_nodes_cheb = [16, 18, 20]
#Mount Everest
plot_lagrange_chebyshev_interpolations(mount_everest_data, [7, 8, 9])
#Bike Ride
plot_lagrange_chebyshev_interpolations(bike_ride_data, num_nodes_cheb)
#Mount Everest
plot_spline_chebyshev_interpolations(mount_everest_data, [7, 8, 9])
#Bike Ride
plot_spline_chebyshev_interpolations(bike_ride_data, num_nodes_cheb)