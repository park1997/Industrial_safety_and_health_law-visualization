import numpy as np
from sklearn.preprocessing import normalize
from sklearn.metrics import pairwise_distances

def generate_spherical(n_class=5, n_per_class=100,
    dimension=2, minimum_cosine_distance=0.1,
    direction_perturbation_factor=0.2,
    radius_perturbation_factor=2):
    
    for _n_try in range(100):
        # class vector
        cv = np.random.random_sample((n_class, dimension))
        cv -= 0.5
        # check pairwise distance of class vectors
        dist = pairwise_distances(cv, metric='cosine')
        dist.sort()
        min_dist = dist[:,1].min()
        if min_dist > minimum_cosine_distance:
            break
        if _n_try >= 99:
            raise ValueError("""Failed to dispersed direction vector generation.""")
    cv = normalize(cv)
    
    X = np.zeros((n_class * n_per_class, dimension))
    Y = np.zeros(n_class * n_per_class)
    for c in range(n_class):
        Y[c * n_per_class:(c+1) * n_per_class] = c
        norm = np.sqrt(sum(cv[c] **2 ))
        for i in range(n_per_class):
            # row idx
            idx = c * n_per_class + i
            # direction pertubation
            dp = np.random.random_sample(dimension) - 0.5
            dp = normalize(dp.reshape(1,-1)) * norm * direction_perturbation_factor * np.random.random()
            # radius (magnitude) pertubation
            v = cv[c] + dp
            v *= (1 + radius_perturbation_factor * np.random.random())
            X[idx] = v

    return X, Y
