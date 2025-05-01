#!/bin/bash

# Path where DOS calculation folders are located
DOS_Folders_PATH="/scratch/qq31/rk2062/Additives_properties_proj/DOS_auto_calculations/"  # Replace with your actual path

# File to store the results
output_file="/scratch/qq31/rk2062/Additives_properties_proj/DOS_auto_calculations/DOS_calculation_status.txt"  # Specify where you want the output to be saved
echo "Folder_Name    Status" > "$output_file"

# Loop through all folders in the given directory
for folder_path in "$DOS_Folders_PATH"*/; do
    folder_name=$(basename "$folder_path")
    log_file="$folder_path/vasp.log"
    
    # Check if vasp.log exists
    if [ -f "$log_file" ]; then
        # Check if "1 F=" tag is present at the end of vasp.log
        if tac "$log_file" | grep -q "  1 F="; then
            # DOS calculation completed
            echo "$folder_name    Completed" >> "$output_file"
        else
            # DOS calculation not completed
            echo "$folder_name    Incomplete" >> "$output_file"
        fi
    else
        # vasp.log file is missing
        echo "$folder_name    vasp.log not found" >> "$output_file"
    fi
done

echo "DOS calculation status check completed. Results saved in $output_file."

