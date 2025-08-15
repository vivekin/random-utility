#!/bin/bash

# Usage: ./list_by_type.sh /path/to/directory extension
# Example: ./list_by_type.sh ~/Downloads pdf

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <directory> <extension>"
    exit 1
fi

dir="$1"
ext="$2"

echo "📂 Searching for *.$ext files in: $dir"
echo "-----------------------------------"

# Find and list files with given extension (case-insensitive)
find "$dir" -type f -iname "*.$ext"

