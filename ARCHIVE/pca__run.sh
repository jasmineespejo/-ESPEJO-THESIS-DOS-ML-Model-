#!/bin/bash
# Make sure to change file permissions
# chmod +x pca__run.sh

# Define the main directory containing all DOS folders
DOSCAR_FILES_DIR="$(cygpath -w "$(dirname "$(pwd)")/DOSCAR_files")"

# 1. Interpolate DOS to common energy grid
# i.e. run pca_interpolate_DOS.py

echo "Running pca_interpolate_DOS.py..."
python pca_interpolate_DOS.py "$DOSCAR_FILES_DIR"
if [ $? -eq 0 ]; then
    echo "pca_interpolate_DOS.py ran successfully."
else
    echo "Error occurred while running pca_interpolate_DOS.py."
    exit 1
fi

: << 'END_COMMENT'
# 3. Perform PCA
# i.e. run PCA_preliminary.py

echo "Running PCA_preliminary.py..."
python PCA_preliminary.py "$DOSCAR_FILES_DIR"
if [ $? -eq 0 ]; then
    echo "PCA_preliminary.py ran successfully."
else
    echo "Error occurred while running PCA_preliminary.py."
    exit 1
fi
