#!/bin/bash

# Path to the directory containing DOS calculation folders
# DOS_Folders_PATH="//scratch/qq31/rk2062/Additives_properties_proj/DOS_auto_calculations/"  # Replace with actual path

DOS_Folders_PATH = "C:/Users/jespe/Desktop/[THESIS] Code/-ESPEJO-THESIS-DOS-ML-Model-/DOS_20241003"

# Loop through all folders in the specified directory
for folder_path in "$DOS_Folders_PATH"*/; do
    folder_name=$(basename "$folder_path")
    doscar_file="$folder_path/DOSCAR"
    # doscar_file="$folder_path/DOSCAR_1-2-3-hexanetriol_RV_DOS"
    
    # Check if DOSCAR file exists
    if [ -f "$doscar_file" ]; then
        # Read the 6th line from the DOSCAR file
        dos_data_start=$(sed -n '6p' "$doscar_file")
        
        # Create a Separate_files directory in the current folder
        output_directory="$folder_path/Separate_files"
        mkdir -p "$output_directory"
        
        # Initialize variables
        current_section=""
        section_counter=0
        
        # Read the DOSCAR file line by line
        while IFS= read -r line; do
            # Check if the line matches the 6th line (start of atom DOS data)
            if [[ "$line" == "$dos_data_start" ]]; then
                # If a section has been collected, save it to a new file
                if [[ -n "$current_section" ]]; then
                    ((section_counter++))
                    # Skip saving the first 2 sections
                    if [[ $section_counter -gt 2 ]]; then
                        output_file="$output_directory/section_${section_counter}.txt"
                        echo "$current_section" > "$output_file"
                    fi
                fi
                # Start a new section
                current_section=""
            fi
            # Append the current line to the section
            current_section+="$line"$'\n'
        done < "$doscar_file"
        
        # Save the last section to a file, skipping first 2 sections
        if [[ -n "$current_section" ]]; then
            ((section_counter++))
            if [[ $section_counter -gt 2 ]]; then
                output_file="$output_directory/section_${section_counter}.txt"
                echo "$current_section" > "$output_file"
            fi
        fi
        
        echo "DOS data separated for $folder_name and saved in $output_directory (skipping first 2 files)"
    else
        echo "DOSCAR file not found in $folder_name"
    fi
done

echo "DOS separation completed for all folders."

