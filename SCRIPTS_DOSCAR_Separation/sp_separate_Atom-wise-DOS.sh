#!/bin/bash

# Use the second argument as the DOS folder path
MAIN_DIR="$1"

echo "MAIN_DIR: $MAIN_DIR"

# Initialize a variable to track if any files were successfully separated
separation_completed=false

# Loop through all folders in the specified directory
for folder_path in "$MAIN_DIR"/*/; do
    folder_name=$(basename "$folder_path")
    
    # Find any file that starts with 'FILE_DOSCAR'
    doscar_file=$(find "$folder_path" -maxdepth 1 -type f -name '*DOSCAR*')
    echo "Current doscar_file: $doscar_file"
    # Check if DOSCAR file exists
    if [ -f "$doscar_file" ]; then
        # Read the 6th line from the DOSCAR file
        dos_data_start=$(sed -n '6p' "$doscar_file")
        
        # Create a Separate_files directory in the current folder
        output_directory="$folder_path/Separate_files"  
            # Check if the Separate_files directory already exists
        if [ -d "$output_directory" ]; then
            echo "Skipping $folder_name as Separate_files directory already exists."
            continue
        fi
        
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
                separation_completed=true
            fi
        fi
        
        echo "Separation status: $separation_completed"
        echo "DOS data separated for $folder_name and saved in $output_directory (skipping first 2 files)"
    else
        echo "DOSCAR file not found in $folder_name"
    fi
done

# Check if no separation was completed and return an error
if ! $separation_completed; then
    echo "Error: No DOS separation was completed in any folder."
    exit 1
fi

echo "DOS separation completed for all folders."