import os
import numpy as np

def calculate_moments(input_file_path):
    data = np.loadtxt(input_file_path)
    energy_levels = data[:, 0]
    dos_values = data[:, 1]

    # Calculate moments
    mean_energy = np.sum(energy_levels * dos_values) / np.sum(dos_values)
    variance = np.sum(((energy_levels - mean_energy) ** 2) * dos_values) / np.sum(dos_values)
    std_dev = np.sqrt(variance)
    skewness = np.sum(((energy_levels - mean_energy) ** 3) * dos_values) / np.sum(dos_values)
    skewness_sqrt = np.sqrt(np.abs(skewness))
    kurtosis = np.sum(((energy_levels - mean_energy) ** 4) * dos_values) / np.sum(dos_values)
    kurtosis_sqrt = np.sqrt(np.abs(kurtosis))

    # Return the calculated moments as a list
    return [mean_energy, variance, std_dev, skewness, skewness_sqrt, kurtosis, kurtosis_sqrt]

def process_dos_folders(dos_folders_path):
    # Define the paths for output files (saved in the same path as input folders)
    output_total_path = os.path.join(dos_folders_path, "all_moments_total_data.txt")
    output_upper_path = os.path.join(dos_folders_path, "all_moments_upper.txt")
    output_lower_path = os.path.join(dos_folders_path, "all_moments_lower.txt")

    # Header for output files with underscores replacing spaces
    header = "Folder_Name,1st_Moment_(Mean_Energy),2nd_Moment_(Variance),Standard_Deviation,3rd_Moment_(Skewness),Square_Root_of_3rd_Moment,4th_Moment_(Kurtosis),Square_Root_of_4th_Moment\n"

    # Open the three output files for appending data
    with open(output_total_path, "w") as total_file, open(output_upper_path, "w") as upper_file, open(output_lower_path, "w") as lower_file:
        # Write the headers to the files
        total_file.write(header)
        upper_file.write(header)
        lower_file.write(header)

        # Iterate through each folder in the DOS directory
        for folder in os.listdir(dos_folders_path):
            folder_path = os.path.join(dos_folders_path, folder, "Separate_files")

            # Check if the Separate_files folder exists
            if os.path.exists(folder_path):
                # Define the exact file names to process
                files_to_process = {
                    "all_orbitals_total.txt": total_file,
                    "upper.txt": upper_file,
                    "lower.txt": lower_file
                }

                for file_name, output_file in files_to_process.items():
                    input_file_path = os.path.join(folder_path, file_name)

                    # Ensure the exact file exists
                    if os.path.isfile(input_file_path):
                        # Calculate moments for the file
                        moments = calculate_moments(input_file_path)

                        # Write the folder name and the moments to the respective output file
                        output_file.write(f"{folder},{','.join(map(str, moments))}\n")
                        print(f"Processed {input_file_path}, output appended to respective summary file.")
                    else:
                        print(f"{file_name} not found in {folder_path}")
            else:
                print(f"Separate_files folder not found in {folder_path}")

if __name__ == "__main__":
    # Define the path to the directory containing DOS folders
    dos_folders_path = "/scratch/qq31/rk2062/Additives_properties_proj/200_bulk_adsor_cal/1st_set_molecules_30/1st_set_molecules_30_calculations/DOS_auto_calculations/"  # Replace with the correct path

    # Process all DOS folders and calculate moments
    process_dos_folders(dos_folders_path)
