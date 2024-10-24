#!/bin/bash

# Print the current working directory
# echo "Current Directory: $(pwd)"

# Define the main directory containing all DOS folders
DOSCAR_FILES_DIR="$(cygpath -w "$(pwd)/DOSCAR_files")" # TODO UPDATE WHEN NECESSARY

# 1. Change file permissions (for bash files in this case)
# echo "Changing file permissions..."
chmod +x sp_separate_Atom-wise-DOS.sh

# echo "Permissions changed for bash files."

# 2. Read DOSCAR and collect each atom wise DOS data
# i.e run sp_separate_Atom-wise-DOS.sh

echo "Running sp_separate_Atom-wise-DOS.sh ..."
./sp_separate_Atom-wise-DOS.sh "$DOSCAR_FILES_DIR"
if [ $? -eq 0 ]; then
    echo "sp_separate_Atom-wise-DOS.sh ran successfully."
else
    echo "Error occurred while running sp_separate_Atom-wise-DOS.sh."
    exit 1
fi

# 3. Combined all atoms DOS data into one file 
# i.e. run sp_TDOS_all_atoms.py

echo "Running sp_TDOS_all_atoms.py..."
python sp_TDOS_all_atoms.py "$DOSCAR_FILES_DIR"
if [ $? -eq 0 ]; then
    echo "sp_TDOS_all_atoms.py ran successfully."
else
    echo "Error occurred while running sp_TDOS_all_atoms.py."
    exit 1
fi

# 4. Merge the orbital data
# i.e. run sp_merging_PEDOS.py

echo "Running sp_merging_PEDOS.py..."
python sp_merging_PEDOS.py "$DOSCAR_FILES_DIR"
if [ $? -eq 0 ]; then
    echo "sp_merging_PEDOS.py ran successfully."
else
    echo "Error occurred while running sp_merging_PEDOS.py."
    exit 1
fi

echo "All tasks completed successfully!"