#!/bin/bash

# Check if path is provided
if [ $# -lt 2 ]; then
    echo "Usage: $0 <directory_path> <file_type>"
    exit 1
fi

DIR="$1"
FILE_TYPE="$2"

# Find and print unique directories containing .mp4 files
find "$DIR" -type f -iname "*.$FILE_TYPE" -printf '%h\n' | sort -u
