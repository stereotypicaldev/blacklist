#!/bin/bash

# Get the current directory (parent directory of the script)
parent_dir=$(pwd)

# Output file in the parent directory
output_file="${parent_dir}/current.txt"

# Temporary file to hold combined contents before removing duplicates
temp_file="${parent_dir}/combined_temp.txt"

# Path to the "dont_include" file
dont_include_file="${parent_dir}/Filters/dont_include.txt"

# Define the path to the custom.txt file inside the "Custom" directory
custom_file="${parent_dir}/Custom/custom.txt"

# Function to handle errors
handle_error() {
  echo "[ERROR] $1"
  exit 1
}

# Check if the script has permission to read/write in the current directory
if [ ! -w "$parent_dir" ]; then
  handle_error "No write permissions in the current directory ($parent_dir). Please check your permissions."
fi

# If current.txt already exists, remove it to start fresh
if [ -f "$output_file" ]; then
  echo "Removing existing current.txt..."
  rm "$output_file" || handle_error "Failed to remove existing $output_file"
fi

# Step 1: Traverse all subfolders and find all text files (.txt), excluding "Custom" and "Filters"
echo "All text files have been combined..."
find "$parent_dir" -type d \( -name "Custom" -o -name "Filters" \) -prune -o -type f -name "*.txt" -print | while read -r txt_file; do
  # Check if the text file is empty before processing
  if [ ! -s "$txt_file" ]; then
    echo "[WARNING] Skipping empty file: $txt_file"
    continue
  fi
  # Append the contents of each text file to the temporary file
  cat "$txt_file" >> "$temp_file" || handle_error "Failed to append contents of $txt_file to $temp_file"
done

# Step 2: Check if any .txt files were found and processed
if [ ! -s "$temp_file" ]; then
  handle_error "No text files were found or processed. Please check the directory structure."
fi

# Step 3: Remove duplicate lines and sort the content alphabetically
echo "Sorted alphabetically..."
sort "$temp_file" | uniq > "$output_file" || handle_error "Failed to sort and remove duplicates from the combined file."

# Clean up the temporary file
rm "$temp_file" || handle_error "Failed to remove temporary file $temp_file."

# Step 4: Check if the "dont_include.txt" file exists
if [ -f "$dont_include_file" ]; then
  # Ensure that "dont_include.txt" is not empty
  if [ ! -s "$dont_include_file" ]; then
    echo "[WARNING] The dont_include.txt file is empty. No lines will be excluded."
  else
    echo "Filters applied successfully...."
    # For each line in "dont_include.txt", remove matching lines from current.txt
    while IFS= read -r line; do
      # Ensure that the line is not empty
      if [ -n "$line" ]; then
        grep -vF -- "$line" "$output_file" > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file" || handle_error "Failed to filter line '$line' from $output_file."
      fi
    done < "$dont_include_file"
  fi
else
  echo "[WARNING] No dont_include.txt file found in the Filters directory. No filters will be applied."
fi

# Step 5: Function to convert domains into Pi-hole compatible regex patterns
convert_to_pihole_regex() {
  local domain=$1
  # Escape all special regex characters in the domain
  domain=$(echo "$domain" | sed 's/[.[\^$()|*+?]/\\&/g')
  
  # If the domain ends with a dot (.), strip it off
  domain=$(echo "$domain" | sed 's/\.$//')

  # Add Pi-hole compatible regex
  echo ".*\.$domain$"
}

# Step 6: Process each line in current.txt and convert it into a Pi-hole compatible regex
echo "Converting domains to Pi-hole compatible regex..."
temp_regex_file="${parent_dir}/pihole_regex.txt"
> "$temp_regex_file"  # Clear the temp file before writing

while IFS= read -r line; do
  # Skip empty lines
  if [ -z "$line" ]; then
    continue
  fi
  
  # Convert the line into a Pi-hole regex and append it to the regex file
  regex=$(convert_to_pihole_regex "$line")
  echo "$regex" >> "$temp_regex_file"
done < "$output_file"

# Step 7: Move the final regex file to current.txt
mv "$temp_regex_file" "$output_file"

# Step 8: Apply filters (from custom.txt) and validate regex
echo "Testing each line in custom.txt for valid regex..."
if [ -f "$custom_file" ]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    if [ -z "$line" ]; then
      continue
    fi

    # Test if the line is a valid regex
    echo "$line" | grep -Pq . > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      echo "[INFO] Valid regex: $line"
      echo "$line" >> "$output_file"
    else
      echo "[ERROR] Invalid regex: $line"
    fi
  done < "$custom_file"
else
  echo "[ERROR] custom.txt file not found in the 'Custom' directory."
  exit 1
fi

# Step 9: Re-run the duplicate removal and sorting after applying custom filters
echo "Removing duplicate lines again and sorting the final file..."
sort "$output_file" | uniq > "${output_file}.tmp" && mv "${output_file}.tmp" "$output_file" || handle_error "Failed to remove duplicates after custom filter application."

# Final message after all processing is complete
echo "Filters applied successfully...."
echo "Domains converted to Pi-hole compatible regex..."
echo "Enjoy... :)"
