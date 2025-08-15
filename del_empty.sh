#!/bin/bash

# Usage: ./delete_zero_files.sh /path/to/directory

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

dir="$1"

echo "🔎 Searching for 0-byte files in: $dir"
echo "-----------------------------------"

# Find zero-byte files
files=$(find "$dir" -type f -size 0c)

if [ -z "$files" ]; then
    echo "✅ No 0-byte files found."
    exit 0
fi

# List them
echo "$files"
echo "-----------------------------------"
echo "🗑 Deleting these files..."

# Delete them
find "$dir" -type f -size 0c -delete

echo "✅ All 0-byte files deleted."

