#!/bin/bash

# Usage: ./find_zero_files.sh /path/to/directory

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

dir="$1"

echo "🔎 Searching for 0-byte files in: $dir"
echo "-----------------------------------"

# Find and list zero-byte files
find "$dir" -type f -size 0c -print

