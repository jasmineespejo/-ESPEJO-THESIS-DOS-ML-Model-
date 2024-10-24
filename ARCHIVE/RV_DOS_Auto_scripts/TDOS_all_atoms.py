import os

# Define the main directory containing all the DOS folders
# main_dir = "/scratch/qq31/rk2062/Additives_properties_proj/DOS_auto_calculations"
main_dir = "C:/Users/jespe/Desktop/[THESIS] Code/-ESPEJO-THESIS-DOS-ML-Model-/DOS_Auto_scripts"



# Function to process a single folder
def process_folder(folder_path):
    separate_files_dir = os.path.join(folder_path, 'Separate_files')
    
    if not os.path.exists(separate_files_dir):
        print(f"No Separate_files directory found in {folder_path}, skipping...")
        return
    
    combined_file_path = os.path.join(separate_files_dir, "combined_DOS_data.txt")
    corrected_file_path = os.path.join(separate_files_dir, "corrected_DOS_data.txt")
    
    # Initialize a dictionary to store the summed values
    summed_data = {}
    
    # Read the Fermi energy from the first section file
    section_files = [f for f in os.listdir(separate_files_dir) if f.startswith('section_') and f.endswith('.txt')]
    if not section_files:
        print(f"No section files found in {separate_files_dir}, skipping...")
        return
    
    first_section_file = os.path.join(separate_files_dir, section_files[0])
    with open(first_section_file, 'r') as file:
        fermi_energy = float(file.readline().split()[3])

    # Process each section file
    for section_file in section_files:
        file_path = os.path.join(separate_files_dir, section_file)
        
        with open(file_path, 'r') as file:
            lines = file.readlines()[1:]  # Skip the header line
            
            for line in lines:
                if line.strip():  # Skip empty lines
                    data = line.split()
                    
                    if len(data) < 2:  # Ensure there are enough columns
                        print(f"Skipping malformed line in {file_path}: {line.strip()}")
                        continue
                    
                    index = data[0]
                    try:
                        values = list(map(float, data[1:]))
                    except ValueError:
                        print(f"Skipping line with invalid values in {file_path}: {line.strip()}")
                        continue
                    
                    if index in summed_data:
                        summed_data[index] = [x + y for x, y in zip(summed_data[index], values)]
                    else:
                        summed_data[index] = values
    
    # Write combined data to file
    with open(combined_file_path, 'w') as output_file:
        for index, values in summed_data.items():
            output_file.write(index + '\t' + '\t'.join(map(str, values)) + '\n')
    
    # Correct the first column (energy levels) using the Fermi energy
    with open(combined_file_path, 'r') as infile, open(corrected_file_path, 'w') as outfile:
        for line in infile:
            parts = line.split()
            if len(parts) > 1:
                try:
                    energy = float(parts[0]) - fermi_energy
                except ValueError:
                    print(f"Skipping line with invalid energy value in {combined_file_path}: {line.strip()}")
                    continue
                rest = '\t'.join(parts[1:])
                outfile.write(f"{energy}\t{rest}\n")

    print(f"Processed folder {folder_path}. Output saved to {combined_file_path} and {corrected_file_path}")

# Iterate over each subfolder in the main directory
for folder in os.listdir(main_dir):
    folder_path = os.path.join(main_dir, folder)
    if os.path.isdir(folder_path):
        process_folder(folder_path)

