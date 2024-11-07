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
        molecule_names = data.iloc[1:, 0] # First column (molecule names)
        dos_data = data.iloc[:, 1:] # Remaining columns (DOS data)
        # print(f"the dos data: {dos_data}")
        molecule_names.reset_index(drop=True, inplace=True)
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

    # Save scaled data (create the file if it doesn't exist)
    filepath = os.path.join(os.getcwd(),'scaled_data.txt')
    # np.savetxt(filepath, scaled_data)

    # Apply PCA
    n_samples = scaled_data.shape[0]
    pca = PCA(n_components=n_samples)
    principal_components = pca.fit_transform(scaled_data)

    # Save PCA results (create the file if it doesn't exist)
    filepath = os.path.join(os.getcwd(),'pca_data.txt')
    # np.savetxt(filepath, principal_components)

    return pca, scaled_data

def transform_data_to_pc(dataset, molecule_names, scaled_data, min_energy, max_energy, cum_variance, n_pc):

    pca = PCA(n_components=n_pc)
    transformed_data = pca.fit_transform(scaled_data)

    # Create a DataFrame with the transformed data
    pc_df = pd.DataFrame(transformed_data, columns=[f'PC{i+1}' for i in range(transformed_data.shape[1])])
    
    # Check lengths to avoid issues
    if len(molecule_names) != transformed_data.shape[0]:
        raise ValueError("Length of molecule_names must match the number of rows in transformed_data.")

    # Add the molecule names as the first column
    pc_df.insert(0, 'Molecule', molecule_names)

    # Generate the filename
    filename = f'transformed_data_[{min_energy:.2f},{max_energy:.2f}]_var{cum_variance:.2f}.txt'

    transformed_data_dir = os.path.join(os.getcwd(),f'transformed_data_{dataset}')

    # Create the directory if it doesn't exist
    if not os.path.exists(transformed_data_dir):
        os.makedirs(transformed_data_dir)  # Creates all intermediate directories if needed

    # Save the DataFrame to a text file
    pc_df.to_csv(os.path.join(transformed_data_dir, filename), sep='\t', index=False)

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

