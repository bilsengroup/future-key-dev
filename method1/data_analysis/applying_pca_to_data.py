import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt



def apply_pca(X):
    # keep columns with names f1 to f300 on X
    X_dismissed = X.loc[:, :'SURVIVAL_RATE']
    X = X.loc[:, 'f1':'f600']



    # Assume `X` is your data matrix with 300 features
    pca = PCA()
    pca.fit(X)

    # Plot explained variance
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_.cumsum(), marker='o')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('Scree Plot')
    plt.grid(True)
    plt.show()
    plt.savefig("Scree Plot.png")

    # Determine the number of components to retain
    explained_variance_threshold = 0.9  # 90%
    num_components = next(i for i, cumulative_variance in enumerate(pca.explained_variance_ratio_.cumsum(), start=1)
                          if cumulative_variance >= explained_variance_threshold)

    print(f"Number of components to retain for {explained_variance_threshold*100}% explained variance: {num_components}")

    # Perform PCA with the number of components to retain and obtain the resulting data matrix
    pca = PCA(n_components=num_components)
    X_pca = pca.fit_transform(X)


    # concatinate the X_dismissed and X_pca to get the final data matrix
    X = pd.concat([X_dismissed, pd.DataFrame(X_pca)], axis=1)

    return X

