# -*-coding:Utf-8 -*

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    import seaborn as sns
except:
    pass
import pandas as pd


def show_quantization(X, X_c, ax=None, use_seaborn=True, name=None):
    """
    Visualise a vector quantization.
    A figure is created and the P instances are shown as dots,
    whereas the Q centroids are shown as diamonds.
    The instances' colors show their appartenance to the centroid 
    of the same color.

    Args:
        X: numpy.ndarray containing the instances (shape = Px2)
        X_c: numpy.ndarray containing the centroids (shape = Qx2)
        ax: a pyplot handle to a subplot axis, if not None no new figure is created
        use_seaborn: wether to use seaborn to display the figure or not
    
    Returns:
        Nothing        

    Authors: 
        Cyril de Bodt (2016) - cyril.debodt@uclouvain.be
        Antoine Vanderschueren (2020) - antoine.vanderschueren@uclouvain.be

    """

    # Checking the arguments
    if not (isinstance(X, np.ndarray) and isinstance(X_c, np.ndarray)):
        raise ValueError("""X and X_c must be numpy.ndarray""")
    if not ((len(X.shape) == 2) and (len(X_c.shape) == 2)):
        raise ValueError("""X and X_c must be numpy.ndarray with 2 dimensions""")
    if not ((X.shape[1] == 2) and (X_c.shape[1] == 2)):
        raise ValueError("""X and X_c must be numpy.ndarray with 2 dimensions and 2 columns""")

    # Finding the index of the nearest centroid in X_c for each point in X
    n_centroids = len(X_c)
    n_points = len(X)
    distances = np.sum((X - X_c[:, np.newaxis])**2, axis=-1)
    closest = np.argmin(distances, axis=0)
    
    if use_seaborn:
        # Moving the data into a DataFrame for seaborn compatibility
        # (Seaborn allows for more eye candy when making graphs)   
        X = pd.DataFrame(data=X, columns=["X1", "X2"])
        X["centroid"] = closest
        X_c = pd.DataFrame(data=X_c, columns=["X1", "X2"])
        X_c["centroid"] = range(n_centroids)
        sns.set() # Set seaborn defaults before call to figure
        
    # Showing the vector quantization
    no_ax = ax==None
    if no_ax:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

    if use_seaborn:
        palette = {i:x for i, x in enumerate(sns.color_palette("deep", n_centroids))}
        sns.scatterplot(data=X, x="X1", y="X2", hue="centroid", palette=palette)
        sns.scatterplot(data=X_c, x="X1", y="X2", hue="centroid", palette=palette,
                        s=150, marker='d', edgecolor='black', alpha=0.8)
        ax.legend_.remove()
    else:
        ax.scatter(np.concatenate((X[:,0], X_c[:,0])), np.concatenate((X[:,1], X_c[:,1])),
                   c=np.concatenate((closest, np.arange(n_centroids))), alpha=0.6)
        ax.scatter(X_c[:,0], X_c[:,1], c=range(n_centroids), marker='d', edgecolor='black', s=150, alpha=0.8)
        plt.grid()
    
    ax.set_xlabel("$X_1$", fontsize=11)
    if name is None:
        ax.set_ylabel("$X_2$", fontsize=11)
    else:
        ax.set_ylabel(f"{name}\n $X_2$", fontsize=11, fontweight="bold")
    
    if no_ax:
        ax.set_title(f"Vector quantization ({n_points} samples - {n_centroids} centroids)", fontsize=15)
        plt.show()
        plt.close()

