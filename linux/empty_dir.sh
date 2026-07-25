#!/bin/bash

# Usage: ./list_empty_dirs.sh /path/to/directory

if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

dir="$1"

echo "📂 Searching for empty directories in: $dir"
echo "-----------------------------------"

# Find empty directories
find "$dir" -type d -empty

