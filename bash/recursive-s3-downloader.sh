#!/bin/sh

# Check if the user provided a file as an argument
if [[ -z "$1" || -z "$2" ]]; then
  echo "Usage: $0 <file-with-s3-directories> <s3-bucket-name> [--exclude <pattern>]"
  exit 1
fi

file="$1"
s3_bucket="$2"
exclude_pattern=""

# Check if the user provided an exclude pattern
if [[ "$3" == "--exclude" && ! -z "$4" ]]; then
  exclude_pattern="--exclude $4"
fi

# Check if the file exists
if [[ -f "$file" ]]; then
  # Read the file line by line
  while IFS= read -r s3_directory; do
    # Skip empty lines and comments
    [[ -z "$s3_directory" || "$s3_directory" =~ ^# ]] && continue

    # Define the source and destination for aws cp
    source="${s3_bucket%/}/${s3_directory%/}/"  # Add a trailing slash to the S3 source
    destination="./results/$s3_directory/"  # Local directory

    # Create local destination directory if it doesn't exist
    mkdir -p "$destination"

    # Execute the AWS cp command with optional exclude argument
    echo "Copying: $source to $destination"
    aws s3 cp "$source" "$destination" --recursive $exclude_pattern
  done < "$file"
else
  echo "File not found: $file"
  exit 1
fi