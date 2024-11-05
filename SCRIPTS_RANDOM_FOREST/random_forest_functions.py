



def load_pca_transformed_data(filepath):
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