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
        - the first row corresponds to the energy values
        - the first column corresponds to molecule names
        - the remaining 1000 columns are DOS data for various energy values 
            (with the range adjusted for the max/min of all molecules)
    """

    try:
        # Read the data from the txt file
        data = pd.read_csv(filepath, delim_whitespace=True, header=None)
        
        # Separate the molecule names and DOS data
        molecule_names = data.iloc[:, 0] # First column (molecule names)
        dos_data = data.iloc[:, 1:] # Remaining columns (DOS data)
        # print(f"the dos data: {dos_data}")
        return molecule_names, dos_data
    
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None, None
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

def perform_PCA(sample_data):

    base_dir=os.path.join(os.getcwd(), 'DOSCAR_files')

    # Standardise/scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(sample_data)

    # Apply PCA
    n_samples = scaled_data.shape[0]
    pca = PCA(n_components=n_samples)
    principal_components = pca.fit_transform(scaled_data)

    # Save PCA results (create the file if it doesn't exist)
    filepath = os.path.join(os.getcwd(),'pca_data.txt')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    np.savetxt(filepath, principal_components, delimiter=',', comments='')
    print(f"PCA results saved at: {filepath}")

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

