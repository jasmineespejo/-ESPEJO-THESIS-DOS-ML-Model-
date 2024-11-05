import os
import shutil

# Define the path to the folder containing your files

source_folder = os.path.join(os.getcwd(), 'Separated_files')
destination_folder = os.path.join(os.getcwd(), 'DOSCAR_files')


# List all files in the source folder
for file_name in os.listdir(source_folder):

    # Check if the file is a valid file (you can add more checks if needed)
    if "DOSCAR" in file_name:
        # Extract the molecule name by splitting at the last '_DOSCAR'
        molecule_name = file_name.rsplit('_DOSCAR', 1)[0]
        
        # Define the path for the new folder
        new_folder_path = os.path.join(destination_folder, molecule_name)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        
        # Define the source and destination file paths
        source_file = os.path.join(source_folder, file_name)

        # Move and rename the file to the new folder
        shutil.move(source_file, new_folder_path)

print("Files have been sorted into folders and renamed to DOSCAR_[molecule name].")
