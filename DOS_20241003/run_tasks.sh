#!/bin/bash

# Step 0: Visualise data
# TODO maybe let's plot some of the data first? let's see what we're dealing with


# 1. Run Separation (separating orbital DOS for each molecule)
echo "Running run_separation.sh  ..."
./run_separation.sh
if [ $? -eq 0 ]; then
    echo "separate_Atom-wise-DOS.sh ran successfully."
else
    echo "Error occurred while running separate_Atom-wise-DOS.sh."
    exit 1
fi

# 2. Interpolate DOS to common energy grid
# i.e. run DOS_interpolation_energy.py

echo "Running DOS_interpolation_energy.py..."
python DOS_interpolation_energy.py
if [ $? -eq 0 ]; then
    echo "DOS_interpolation_energy.py ran successfully."
else
    echo "Error occurred while running DOS_interpolation_energy.py."
    exit 1
fi
