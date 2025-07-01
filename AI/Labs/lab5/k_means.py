import numpy as np

def initialize_centroids_forgy(data, k):
    indices = np.random.choice(data.shape[0], size=k, replace=False)
    return data[indices]

def initialize_centroids_kmeans_pp(data, k):
    n_samples = data.shape[0]
    centroids = [data[np.random.choice(n_samples)]]
    for _ in range(1, k):
        dist_sq = np.min([np.sum((data - c)**2, axis=1) for c in centroids], axis=0)
        probs = dist_sq / np.sum(dist_sq)
        new_centroid = data[np.random.choice(n_samples, p=probs)]
        centroids.append(new_centroid)
    return np.array(centroids)

def assign_to_cluster(data, centroid):
    distances = np.linalg.norm(data[:, np.newaxis] - centroid, axis=2)
    return np.argmin(distances, axis=1)

def update_centroids(data, assignments):
    k = np.max(assignments) + 1
    return np.array([data[assignments == i].mean(axis=0) for i in range(k)])

def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :])**2))

def k_means(data, num_centroids, kmeansplusplus= False):
    # centroids initizalization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else: 
        centroids = initialize_centroids_forgy(data, num_centroids)

    
    assignments  = assign_to_cluster(data, centroids)
    for i in range(100): # max number of iteration = 100
        #print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments): # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)         

