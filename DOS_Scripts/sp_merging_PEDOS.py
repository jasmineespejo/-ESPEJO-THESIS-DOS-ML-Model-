import os
import sys

# Function to sum specified columns in a given file
def sum_columns(file_path, column_indices):
    # Initialize a list to store the summed values for each row
    summed_data = []

    # Read data from the file
    with open(file_path, "r") as file:
        for line in file:
            data = line.split()
            if len(data) > max(column_indices):
                try:
                    energy = float(data[0])
                    values_to_sum = [float(data[i]) for i in column_indices]
                    summed_value = sum(values_to_sum)
                    summed_data.append([energy, summed_value])
                except ValueError:
                    print(f"Skipping line with invalid data in {file_path}: {line.strip()}")
            else:
                print(f"Skipping line with insufficient columns in {file_path}: {line.strip()}")

    return summed_data

# Function to write the summed data to an output file
def write_output(summed_data, output_path):
    # Write the summed values to the output file
    with open(output_path, "w") as output_file:
        for row in summed_data:
            output_file.write("\t".join(map(str, row)) + "\n")

# Function to process each folder and sum columns from corrected DOS files
def process_folder(folder_path, column_indices):
    separate_files_dir = os.path.join(folder_path, 'Separate_files')
    
    if not os.path.exists(separate_files_dir):
        print(f"No Separate_files directory found in {folder_path}, skipping...")
        return
    
    corrected_file_path = os.path.join(separate_files_dir, "corrected_DOS_data.txt")
    output_file_path = os.path.join(separate_files_dir, "all_orbitals_total.txt")
    
    if not os.path.exists(corrected_file_path):
        print(f"No corrected_DOS_data.txt file found in {separate_files_dir}, skipping...")
        return
    
    # Sum the specified columns
    result_data = sum_columns(corrected_file_path, column_indices)
    
    # Write the summed data to the output file
    write_output(result_data, output_file_path)

    print(f"Processed folder {folder_path}. Summed orbital values saved to {output_file_path}")

if __name__ == "__main__":
    # Check if the the directory path argument is provided
    if len(sys.argv) < 2:
        print("Usage: MAIN_DIR argument not provided")
        sys.exit(1)

    # Get the main directory path from the first command-line argument
    main_dir = sys.argv[1]

    # main_dir = "/scratch/qq31/rk2062/Additives_properties_proj/200_bulk_adsor_cal/1st_set_molecules_30/1st_set_molecules_30_calculations/DOS_auto_calculations/"  # Update this path to your main directory containing DOS folders
    # main_dir = "C:/Users/jespe/Desktop/[THESIS] Code/-ESPEJO-THESIS-DOS-ML-Model-/DOS_20241003"
    
    # Manually specify the column indices to sum (0-based index)
    column_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Replace these indices with the actual columns you want to sum
    
    # Iterate over each subfolder in the main directory
    for folder in os.listdir(main_dir):
        folder_path = os.path.join(main_dir, folder)
        if os.path.isdir(folder_path):
            process_folder(folder_path, column_indices)


