import numpy as np
import os
import sys

from pca_obtain_energy_range import find_common_energy_range
from scipy.interpolate import interp1d

def load_energy_data(filepath):
    """
    Loads the energy data from a given text file.
    Assumes the file contains two columns: [energy, orbital_DOS].
    
    """
    try:
        data = np.loadtxt(filepath)
        energy = data[:, 0]     # First column: energy levels
        orbital_dos = data[:, 1]  # Second column: total DOS
        return energy, orbital_dos
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None
    
def interpolate_single(energy_grid, energy, orbital_dos):
    """
    Interpolates the orbital DOS data to match the specified common energy grid.
    """
    # Create an interpolation function
    interp_func = interp1d(energy, orbital_dos, bounds_error=False, fill_value=0)

    # Interpolate the DOS data
    interpolated_dos = interp_func(energy_grid)
    return interpolated_dos

def interpolate_all(base_dir, energy_grid):
    """
    Performs DOS interpolation across all molecules in the given base directory.
    """

    all_interpolated_dos = {}
    
    # Iterate through each molecule's directory
    for mol_dir in os.listdir(base_dir):
        mol_path = os.path.join(base_dir, mol_dir, 'Separate_files', 'all_orbitals_total.txt')

        if os.path.exists(mol_path):
            # Load the energy data
            energy, orbital_dos = load_energy_data(mol_path)

            if energy is not None and orbital_dos is not None:
                # Interpolate the DOS data to the common energy grid
                interpolated_dos = interpolate_single(energy_grid, energy, orbital_dos)

                all_interpolated_dos[mol_dir] = interpolated_dos
            else:
                print(f"No valid energy data found for molecule {mol_dir}.")
        
            # print(f"File not found for molecule {mol_dir}: {mol_path}")

    output_filepath = os.path.join(base_dir, 'interpolated_dos.txt') # Output file

    # Save interpolated data dictionary to a text file
    with open(output_filepath, 'w') as f:
        # Write header (energy grid values as columns)
        f.write('Molecule\t'+ '\t'.join(map(str, energy_grid)) + '\n') 

        # Write each molecule DOS
        for molecule, dos in all_interpolated_dos.items():
            f.write(f"{molecule}\t" + '\t'.join(map(str, dos)) + '\n')

    print(f"Interpolated DOS data saved to {output_filepath}")

def perform_interpolation(base_dir, min_energy_global, max_energy_global):
    # Find the common energy range across all molecules
    # 

    common_energy_grid = np.linspace(min_energy_global, max_energy_global, num=1000)
    # Call the interpolation function
    interpolate_all(base_dir, common_energy_grid)


"""
if __name__ == "__main__":
    # Check if the the directory path argument is provided
    if len(sys.argv) < 2:
        print("Usage: MAIN_DIR argument not provided")
        sys.exit(1)

    # Get the base directory path from the first command-line argument
    base_dir = sys.argv[1]

    # Find the common energy range across all molecules
    min_energy_global, max_energy_global = find_common_energy_range(base_dir)

    if len(sys.argv) == 4:
        min_energy_global = sys.argv[2]
        max_energy_global = sys.argv[3]

    common_energy_grid = np.linspace(min_energy_global, max_energy_global, num=1000)

    # Call the interpolation function
    interpolate_all(base_dir, common_energy_grid)

"""
