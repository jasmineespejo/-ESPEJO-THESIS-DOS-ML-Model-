#!/bin/bash

# Main directory containing all the DOS folders
main_dir="/scratch/qq31/rk2062/Additives_properties_proj/DOS_auto_calculations"

# Loop over each subfolder in the main directory
for folder in "$main_dir"*/; do
    separate_files_dir="$folder/Separate_files"

    if [ ! -d "$separate_files_dir" ]; then
        echo "No Separate_files directory found in $folder, skipping..."
        continue
    fi

    combined_file="$separate_files_dir/combined_DOS_data.txt"
    corrected_file="$separate_files_dir/corrected_DOS_data.txt"

    # Check if there are section files
    section_files=("$separate_files_dir"/section_*.txt)
    if [ ${#section_files[@]} -eq 0 ]; then
        echo "No section files found in $separate_files_dir, skipping..."
        continue
    fi

    # Read the Fermi energy from the first section file
    first_section_file="${section_files[0]}"
    fermi_energy=$(awk 'NR == 1 {print $4}' "$first_section_file")

    # Initialize an associative array for summing data
    declare -A summed_data
    file_count=0

    # Iterate through all section files in the folder
    for section_file in "${section_files[@]}"; do
        # Skip the first line (header) and read each line after that
        tail -n +2 "$section_file" | while read -r line; do
            # Split the line into index and values
            index=$(echo "$line" | awk '{print $1}')
            values=($(echo "$line" | awk '{for(i=2; i<=NF; i++) print $i}'))

            # Sum the values for each index
            if [[ -n "${summed_data[$index]}" ]]; then
                current_values=(${summed_data[$index]})
                for i in "${!values[@]}"; do
                    current_values[$i]=$(echo "${current_values[$i]} + ${values[$i]}" | bc)
                done
                summed_data[$index]="${current_values[@]}"
            else
                summed_data[$index]="${values[@]}"
            fi
        done

        # Increment file count
        file_count=$((file_count + 1))
    done

    # Write combined (summed) data to the output file
    {
        for index in "${!summed_data[@]}"; do
            printf "%s\t" "$index"
            printf "%s\t" ${summed_data[$index]}
            echo ""
        done
    } > "$combined_file"

    # Apply Fermi correction to the first column and write to the corrected file
    awk -v fermi="$fermi_energy" 'NR == 1 {print $0; next} { $1 = $1 - fermi; print }' "$combined_file" > "$corrected_file"

    echo "Processed folder $folder. Output saved to $combined_file and $corrected_file."
done

