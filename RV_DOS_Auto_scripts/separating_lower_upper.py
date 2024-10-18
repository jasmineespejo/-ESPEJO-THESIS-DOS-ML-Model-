import os

def process_file(file_path):
    lower_data = []
    upper_data = []

    # Read the data from the all_orbitals_total.txt file
    with open(file_path, "r") as file:
        for line in file:
            data = line.split()
            energy = float(data[0])  # 1st column (energy values)
            dos_value = data[1]  # 2nd column (DOS data)

            # Separate based on the energy value (negative or positive)
            if energy < 0:
                lower_data.append(line)
            else:
                upper_data.append(line)

    return lower_data, upper_data

def write_output(data, output_path):
    # Write the data to the specified output file
    with open(output_path, "w") as file:
        for line in data:
            file.write(line)

def process_dos_folders(dos_folders_path):
    # Loop through each DOS folder
    for folder in os.listdir(dos_folders_path):
        folder_path = os.path.join(dos_folders_path, folder, "Separate_files")
        all_orbitals_file = os.path.join(folder_path, "all_orbitals_total.txt")

        # Check if the file exists
        if os.path.exists(all_orbitals_file):
            print(f"Processing {all_orbitals_file}...")

            # Process the file and get upper and lower data
            lower_data, upper_data = process_file(all_orbitals_file)

            # Define output paths for upper.txt and lower.txt
            lower_output = os.path.join(folder_path, "lower.txt")
            upper_output = os.path.join(folder_path, "upper.txt")

            # Write the data to the respective files
            write_output(lower_data, lower_output)
            write_output(upper_data, upper_output)

            print(f"Created {lower_output} and {upper_output}")
        else:
            print(f"{all_orbitals_file} not found in {folder_path}")

if __name__ == "__main__":
    # Define the path to the directory containing DOS folders
    # dos_folders_path = "/scratch/qq31/rk2062/Additives_properties_proj/200_bulk_adsor_cal/1st_set_molecules_30/1st_set_molecules_30_calculations/DOS_auto_calculations/"  # Replace with the correct path
    dos_folders_path = "C:/Users/jespe/Desktop/[THESIS] Code/-ESPEJO-THESIS-DOS-ML-Model-/DOS_Auto_scripts"


    # Process all DOS folders
    process_dos_folders(dos_folders_path)

