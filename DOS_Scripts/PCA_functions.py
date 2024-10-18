import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def load_interpolated_dos(filepath):
    """
    Loads the interpolated DOS data from a given text file.
    Assumes the file contains a nx1001 matrix, where:
        - the first column corresponds to molecule names
        - the remaining 1000 columns are DOS data for various energy values 
            (with the range adjusted for the max/min of all molecules)
    """

    try:
        # Read the data from the txt file
        data = pd.read_csv(filepath, delim_whitespace=True, header=None)
        
        # Separate the molecule names and DOS data
        molecule_names = data.iloc[:, 0] # First column (molecule names)
        dos_data = data.iloc[:, 1:].values  # Remaining columns (DOS data)
        return molecule_names, dos_data
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

def perform_PCA(dos_data):

    base_dir=os.path.join(os.getcwd(), 'DOSCAR_files')

    # Standardise/scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dos_data)

    # Apply PCA
    n_samples = scaled_data.shape[0] - 1
    pca = PCA(n_components=n_samples)
    principal_components = pca.fit_transform(scaled_data)

    filepath = os.path.join(base_dir,'pca_data.txt')

    np.savetxt(filepath, principal_components, delimiter=',', header='PC1,PC2', comments='')
    print(f"File saved at: {filepath}")

    # Inspect the explained variance
    explained_variance = pca.explained_variance_ratio_
    print(f"The explained variance is {explained_variance}")

    return pca, scaled_data

if __name__ == "__main__":
    # Check if the the directory path argument is provided
    if len(sys.argv) < 2:
        print("Usage: MAIN_DIR argument not provided")
        sys.exit(1)

    # Get the base directory path from the first command-line argument
    base_dir = sys.argv[1]
    interpolated_filepath = os.path.join(base_dir,'interpolated_dos.txt')

    molecule_names, dos_data = load_interpolated_dos(base_dir)

    perform_PCA(dos_data)

