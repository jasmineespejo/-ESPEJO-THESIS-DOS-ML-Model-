#!/bin/bash

# Step 0: Visualise data
# TODO maybe let's plot some of the data first? let's see what we're dealing with

# Define the main directory containing all DOS folders
DOSCAR_FILES_DIR="$(cygpath -w "$(pwd)/DOSCAR_files")" # TODO UPDATE WHEN NECESSARY

# 1. Run Separation (separating orbital DOS for each molecule)
chmod +x sp__run.sh
echo "Running sp__run  ..."
./sp__run.sh
if [ $? -eq 0 ]; then
    echo "sp__run.sh  ran successfully."
else
    echo "Error occurred while running sp__run.sh."
    exit 1
fi


# 2. Interpolate DOS to common energy grid
# i.e. run DOS_interpolation_energy.py

echo "Running DOS_interpolation_energy.py..."
python DOS_interpolation_energy.py "$DOSCAR_FILES_DIR"
if [ $? -eq 0 ]; then
    echo "DOS_interpolation_energy.py ran successfully."
else
    echo "Error occurred while running DOS_interpolation_energy.py."
    exit 1
fi
