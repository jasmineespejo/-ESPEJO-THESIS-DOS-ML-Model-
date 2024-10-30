import os
import sys
import numpy as np

def get_energy_range(filepath):
    """
    Reads the energy levels from a text file and returns the min and max energy.
    Assumes the file contains at least two columns: [energy, total DOS]
    """

    try:
        # Read the file and extract the energy column (first column)
        data = np.loadtxt(filepath, usecols=(0,))
        
        # Extract the min and max energy levels
        min_energy = np.min(data)
        max_energy = np.max(data)

        return min_energy, max_energy
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None
    

def find_common_energy_range(base_dir):
    """
    Finds the common energy range across all molecules.
    Assumes each molecule has a directory in 'base_dir' with a file 'all_orbitals_total.txt'.
    """

    min_energy_global = None
    max_energy_global = None

    # Iterate over all molecule directories
    for mol_dir in os.listdir(base_dir):
        mol_path = os.path.join(base_dir, mol_dir, 'Separate_files', 'all_orbitals_total.txt')

        if os.path.exists(mol_path):
            min_energy, max_energy = get_energy_range(mol_path)

            if min_energy_global is None and max_energy_global is None:
                min_energy_global = min_energy
                max_energy_global = max_energy

            if min_energy is not None and max_energy is not None:
                # Update global min and max energy levels
                min_energy_global = max(min_energy_global, min_energy)
                max_energy_global = min(max_energy_global, max_energy)
        
                print(f"Energy range update for molecule {mol_dir}.")
        
        """ 
        else:
            print(f"File not found for molecule {mol_dir}: {mol_path}")

        """  
    # Return the common energy range
    return min_energy_global, max_energy_global

if __name__ == "__main__":
    # Check if the the directory path argument is provided
    if len(sys.argv) < 2:
        print("Usage: MAIN_DIR argument not provided")
        sys.exit(1)

    # Get the base directory path from the first command-line argument
    base_dir = sys.argv[1]

    # Find the common energy range across all molecules
    min_energy_global, max_energy_global = find_common_energy_range(base_dir)

    if min_energy_global != float('inf') and max_energy_global != float('-inf'):
        print(f"Common energy range across all molecules: [{min_energy_global}, {max_energy_global}]")
    else:
        print("No valid energy data found.")