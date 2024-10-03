#!/bin/bash

# Print the current working directory
echo "Current Directory: $(pwd)"

# 1. Change file permissions (for bash files in this case)
echo "Changing file permissions..."
chmod +x separate_Atom-wise-DOS.sh

echo "Permissions changed for bash files."

# 2. Read DOSCAR and collect each atom wise DOS data
# i.e run separate_Atom-wise-DOS.sh

echo "Running separate_Atom-wise-DOS.sh ..."
./separate_Atom-wise-DOS.sh
if [ $? -eq 0 ]; then
    echo "separate_Atom-wise-DOS.sh ran successfully."
else
    echo "Error occurred while running separate_Atom-wise-DOS.sh."
    exit 1
fi

# 3. Combined all atoms DOS data into one file 
# i.e. run TDOS_all_atoms.py

echo "Running TDOS_all_atoms.py..."
python TDOS_all_atoms.py
if [ $? -eq 0 ]; then
    echo "TDOS_all_atoms.py ran successfully."
else
    echo "Error occurred while running TDOS_all_atoms.py."
    exit 1
fi

# 4. Merge the orbital data

echo "Running merging_PEDOS.py..."
python merging_PEDOS.py
if [ $? -eq 0 ]; then
    echo "merging(all-orbitals)_PEDOS.py ran successfully."
else
    echo "Error occurred while running merging(all-orbitals)_PEDOS.py."
    exit 1
fi

echo "All tasks completed successfully!"