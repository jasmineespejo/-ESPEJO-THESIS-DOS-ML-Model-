import pandas as pd
import numpy as np

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

def perform_PCA(molecule_names, dos_data):

    # Standardise/scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dos_data)

    # Apply PCA
    k = 1 # TODO Replace 'k' with the number of components you want to retain
    pca = PCA(n_components=k)
    principal_components = pca.fit_transform(scaled_data)
    
    return None

if __name__ == "__main__":
    base_dir = "./" # TODO: Update this to base directory
    